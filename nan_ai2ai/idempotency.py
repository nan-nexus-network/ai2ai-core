# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Cơ chế Idempotency nguyên tử — chống thực thi lặp cả tuần tự lẫn đồng thời.

Vì sao cần "Atomic In-flight Claim"
-----------------------------------
Ở v0.2, deduplication cache chỉ kiểm tra ``operation_id`` đã có trong cache hay
chưa. Với **hai request đến cùng lúc**, cả hai đều thấy cache rỗng và cùng
thực thi — đây là race condition, và với tác vụ có tính phí (thanh toán, đặt
hàng, gọi API trả tiền) thì hậu quả là **double-spend**.

Cơ chế ở đây là "claim" nguyên tử: request đầu tiên **chiếm** (claim) khoá,
những request sau thấy khoá đang được xử lý thì **chờ** (`threading.Event`)
thay vì tự chạy.

Ba trạng thái
--------------
``PROCESSING`` — khoá đã được chiếm, đang chạy.
``DONE``       — đã có kết quả; trả lại kết quả cũ.
``FAILED``     — lần chạy trước lỗi; **không** tự chạy lại (xem `claim`).

Nguyên tắc "at-most-once"
-------------------------
Cùng một ``operation_id`` chỉ được **thực thi đúng một lần**. Nếu lần chạy đó
lỗi, khoá được đánh dấu ``FAILED`` và những request đang chờ nhận **lỗi đó**,
không tự động chạy lại — vì tác vụ có thể **đã** có tác dụng phụ (đã trừ tiền,
đã gửi hàng) trước khi lỗi xảy ra. Chạy lại tự động là mở lại đúng lỗi
double-spend mà cơ chế này sinh ra để chống.

Giới hạn (PoC)
---------------
- Trạng thái **chỉ trong bộ nhớ của một tiến trình**: mất khi khởi động lại,
  **không** dùng chung giữa nhiều tiến trình/nút. Chống replay chỉ có hiệu lực
  trong phạm vi một process.
- Dùng ``threading.Lock`` → chỉ bảo vệ được trong **một** tiến trình Python.
  Với nhiều tiến trình hoặc nhiều máy, cần khoá phân tán (Redis, v.v.).
- Không có TTL: mục đích vô hạn nếu không dọn.
- ``threading.Event.wait()`` **không** đảm bảo thứ tự FIFO giữa các waiter.

Cách dùng
----------
::

    receipt = ProtocolBridgeNode.execute_with_idempotency(
        operation_id, bridged_packet, lambda: call_remote_agent()
    )
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Dict, Optional, Tuple

__all__ = ["IdempotencyStore", "OperationFailed"]


class OperationFailed(Exception):
    """Lần chạy trước của cùng một ``operation_id`` đã thất bại."""

    def __init__(self, operation_id: str, cause: BaseException) -> None:
        super().__init__(
            "Thao tac '%s' da that bai truoc do: %s" % (operation_id, cause))
        self.operation_id = operation_id
        self.cause = cause


class IdempotencyStore:
    """Kho trạng thái idempotency với claim nguyên tử.

    Mọi thao tác biến đổi trạng thái đều nằm trong ``_cache_lock``. Việc chờ
    (``Event.wait``) diễn ra **ngoài** khoá, để không giữ khoá khi chờ.
    """

    def __init__(self) -> None:
        self._cache_lock = threading.Lock()
        self._in_flight_events: Dict[str, threading.Event] = {}
        self._receipt_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    def claim(self, operation_id: str) -> Tuple[str, Any]:
        """Chiếm khoá idempotency cho ``operation_id``.

        Trả về một cặp ``(trạng thái, payload)``:

        ``("DONE", receipt)``     đã có kết quả -> dùng lại kết quả cũ.
        ``("FAILED", error)``     lần chạy trước lỗi -> ném lỗi ra cho caller.
        ``("INFLIGHT", event)``   request khác đang chạy -> chờ ``event``.
        ``("CLAIMED", event)``    bạn là request duy nhất -> hãy chạy.
        """
        with self._cache_lock:
            entry = self._receipt_cache.get(operation_id)
            if entry is not None:
                status = entry.get("status")
                if status == "DONE":
                    return ("DONE", entry["receipt"])
                if status == "FAILED":
                    return ("FAILED", entry["error"])

            event = self._in_flight_events.get(operation_id)
            if event is not None:
                # Request khac da giu khoa. Cho no chay tiep, ta se cho.
                return ("INFLIGHT", event)

            event = threading.Event()
            self._in_flight_events[operation_id] = event
            self._receipt_cache[operation_id] = {"status": "PROCESSING"}
            return ("CLAIMED", event)

    # ------------------------------------------------------------------
    def complete(self, operation_id: str, receipt: Any) -> None:
        """Ghi kết quả, giải phóng khoá và đánh thức các request đang chờ."""
        with self._cache_lock:
            self._receipt_cache[operation_id] = {
                "status": "DONE",
                "receipt": receipt,
            }
            event = self._in_flight_events.pop(operation_id, None)
        if event is not None:
            event.set()

    # ------------------------------------------------------------------
    def fail(self, operation_id: str, error: BaseException) -> None:
        """Ghi lỗi, giải phóng khoá và đánh thức các request đang chờ.

        Kết quả được đánh dấu ``FAILED`` **không** phải ``DONE``: một thao tác
        đã lỗi không được coi là đã xong, và không được tự chạy lại.
        """
        with self._cache_lock:
            self._receipt_cache[operation_id] = {
                "status": "FAILED",
                "error": error,
            }
            event = self._in_flight_events.pop(operation_id, None)
        if event is not None:
            event.set()

    # ------------------------------------------------------------------
    def lookup(self, operation_id: str) -> Optional[Any]:
        """Trả về kết quả đã hoàn tất cho ``operation_id``, hoặc ``None``.

        ``None`` nghĩa là: chưa có, đang chạy, hoặc đã lỗi.
        """
        with self._cache_lock:
            entry = self._receipt_cache.get(operation_id)
            if entry is None or entry.get("status") != "DONE":
                return None
            return entry["receipt"]

    # ------------------------------------------------------------------
    def status(self, operation_id: str) -> str:
        """Trạng thái hiện tại: ``NEW`` / ``PROCESSING`` / ``DONE`` / ``FAILED``."""
        with self._cache_lock:
            entry = self._receipt_cache.get(operation_id)
            if entry is None:
                return "NEW"
            return str(entry.get("status"))

    # ------------------------------------------------------------------
    def clear(self) -> None:
        """Xoá toàn bộ trạng thái (dùng cho test và khi khởi động lại)."""
        with self._cache_lock:
            self._receipt_cache.clear()
            for event in self._in_flight_events.values():
                event.set()
            self._in_flight_events.clear()

    # ------------------------------------------------------------------
    def run_once(
        self,
        operation_id: str,
        work: Callable[[], Any],
        build_result: Callable[[Any], Any],
    ) -> Any:
        """Chạy ``work`` **đúng một lần** cho mỗi ``operation_id``.

        ``work()`` là phần *tác vụ* (có thể tốn thời gian, có thể lỗi).
        ``build_result(output)`` biến kết quả của ``work`` thành thứ cần lưu
        (ví dụ biên nhận) — được gọi **một lần**, sau khi ``work`` thành công.

        Trả về kết quả đã lưu (cùng đối tượng cho mọi request cùng khoá).
        """
        while True:
            state, payload = self.claim(operation_id)
            if state == "DONE":
                return payload
            if state == "FAILED":
                raise OperationFailed(operation_id, payload)
            if state == "INFLIGHT":
                # KHONG giu khoa khi cho. Sau khi thuc, phai QUAY LAI doc lai
                # trang thai: co the request khac vua ket thuc (va ket qua
                # chua duoc ghi) hoac vua that bai.
                payload.wait()
                continue
            # CLAIMED
            try:
                output = work()
                result = build_result(output)
            except BaseException as exc:
                self.fail(operation_id, exc)
                raise
            self.complete(operation_id, result)
            return result
