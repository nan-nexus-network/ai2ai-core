# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""
NAN AI2AI-SI2SI: P2P Agent Chat Demo (Zero Dependencies)
Tương thích: Python 3.8+ (Chỉ sử dụng Python Standard Library)
Giấy phép: Apache License 2.0

Kịch bản: Alice (Agent A) muốn tìm nhà cung cấp linh kiện tại Quảng Châu.
Cô ấy gửi yêu cầu qua lớp bằng chứng kỹ thuật của NAN AI2AI đến Bob (Agent B) - người sở hữu dữ liệu chuỗi cung ứng.
Hai Agent tự đàm phán và Bob gửi lại kết quả kèm Biên nhận xác thực (SHA-256).

Lưu ý: Đây là mô phỏng luồng (simulation). Chữ ký số xác thực danh tính (Ed25519)
đang được phát triển tại Issue #2. Kết quả SHA-256 ở đây chỉ đảm bảo tính toàn vẹn
dữ liệu (Integrity), không xác thực danh tính hay nguồn gốc.
"""

import json
import hashlib
import uuid
import os
import sys
import threading
from datetime import datetime, timezone

# Them thu muc goc kho vao sys.path de import duoc goi `nan_ai2ai`.
# Van hoat dong 100% thu vien chuan - khong dung goi cai dat nao.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from nan_ai2ai import idempotency  # noqa: E402

class NANBridgeNode:
    """Mô phỏng Node Cầu nối NAN AI2AI"""

    #: Cache loại trừ trùng lặp (deduplication cache) — mức PoC, trong bộ nhớ.
    #:
    #: Cùng giới hạn như `ProtocolBridgeNode._receipt_cache` trong
    #: `examples/01-hello-agent/hello_bridge.py`: mất khi khởi động lại, không
    #: dùng chung giữa các tiến trình, không có TTL. Việc hợp nhất hai hiện
    #: thực bridge còn lại nằm trong backlog (xem `ROADMAP.md`, mục BL4).
    # Kho trang thai idempotency rieng cho bridge nay (khong dung chung voi
    # `ProtocolBridgeNode` trong examples/01-hello-agent/hello_bridge.py - hai
    # hien thuc bridge van tach, xem ROADMAP.md muc BL4).
    _store = idempotency.IdempotencyStore()
    _cache_lock = _store._cache_lock
    _in_flight_events = _store._in_flight_events
    _receipt_cache = _store._receipt_cache

    @staticmethod
    def route_request(sender_did: str, receiver_did: str, payload: dict) -> dict:
        """Đóng gói và chuyển tiếp yêu cầu"""
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        bridge_packet = {
            "protocol": "NAN-AI2AI/v1.0",
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": sender_did,
            "receiver": receiver_did,
            "task": payload
        }
        return bridge_packet

    @staticmethod
    def lookup_cached_receipt(operation_id: str):
        """Trả về biên nhận đã cấp cho `operation_id`, hoặc None."""
        if not isinstance(operation_id, str) or not operation_id:
            return None
        receipt = NANBridgeNode._store.lookup(operation_id)
        return dict(receipt) if receipt else None

    @staticmethod
    def _build_receipt(trace_id: str, result: dict, operation_id: str) -> dict:
        """Tạo biên nhận SHA-256 (hàm thuần, không đụng cache/khoá)."""
        raw_data = json.dumps(result, sort_keys=True) + trace_id
        proof = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        return {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "trace_id": trace_id,
            "operation_id": operation_id,
            "status": "DIGEST_ISSUED_BY_NAN_AI2AI",
            "sha256_proof": proof,
            "data": result
        }

    @classmethod
    def execute_once(cls, operation_id: str, executor_fn, trace_id: str) -> dict:
        """Chạy tác vụ **đúng một lần** cho mỗi `operation_id`, rồi cấp biên nhận.

        `executor_fn()` là phần tác vụ (gọi Agent B). Khoá idempotency được
        chiếm **trước khi** gọi nó, nên nếu có nhiều request cùng
        `operation_id` đến đồng thời, chỉ một request thực sự gọi Agent B.
        """
        store = cls._store
        while True:
            state, payload = store.claim(operation_id)
            if state == "DONE":
                print("   [Bridge] Duplicate detected! Returning cached receipt.")
                return payload
            if state == "FAILED":
                raise idempotency.OperationFailed(operation_id, payload)
            if state == "INFLIGHT":
                payload.wait()
                continue
            try:
                result = executor_fn()
                receipt = cls._build_receipt(trace_id, result, operation_id)
            except BaseException as exc:
                store.fail(operation_id, exc)
                raise
            store.complete(operation_id, receipt)
            return receipt

    @classmethod
    def issue_receipt(cls, trace_id: str, result: dict, operation_id: str) -> dict:
        """Cấp biên nhận xác thực SHA-256, có loại trừ trùng lặp theo operation_id.

        Nếu `operation_id` đã có biên nhận, trả lại biên nhận cũ kèm log
        "Duplicate detected! Returning cached receipt."
        """
        store = cls._store
        while True:
            state, payload = store.claim(operation_id)
            if state == "DONE":
                print("   [Bridge] Duplicate detected! Returning cached receipt.")
                return payload
            if state == "FAILED":
                raise idempotency.OperationFailed(operation_id, payload)
            if state == "INFLIGHT":
                payload.wait()
                continue
            try:
                receipt = cls._build_receipt(trace_id, result, operation_id)
            except BaseException as exc:
                store.fail(operation_id, exc)
                raise
            store.complete(operation_id, receipt)
            return receipt

class AIAgent:
    def __init__(self, name, did):
        self.name = name
        self.did = did
        self.calls = 0  # dem so lan thuc thi - de chung minh retry khong chay lai

    def process_task(self, task):
        self.calls += 1
        print(f"\n[{self.name}] Đang xử lý yêu cầu: '{task['query']}'...")
        # Giả lập thời gian xử lý
        import time
        time.sleep(0.5)
        if "Quảng Châu" in task['query']:
            return {"status": "success", "suppliers_found": 3, "top_match": "Guangzhou Tech Parts Co."}
        return {"status": "not_found"}

def run_demo():
    print("=" * 70)
    print(" NAN AI2AI: P2P AGENT-TO-AGENT CHAT DEMO (P2P)")
    print("=" * 70)

    # Khởi tạo 2 Agents độc lập
    alice_agent = AIAgent("Alice_Agent", "did:nan:alice_01")
    bob_agent = AIAgent("Bob_Agent", "did:nan:bob_02")
    bridge = NANBridgeNode()

    # 1. Alice tạo yêu cầu
    task_payload = {
        "operation_id": "op_123456",
        "query": "Tìm nhà cung cấp linh kiện điện tử tại Quảng Châu",
        "max_budget_vnd": 500000000
    }
    print(f"\n[1] {alice_agent.name} khởi tạo yêu cầu:")
    print(json.dumps(task_payload, indent=2, ensure_ascii=False))

    # 2. Bridge chuyển tiếp
    print(f"\n[2] NAN AI2AI đang định tuyến từ {alice_agent.did} -> {bob_agent.did}...")
    packet = bridge.route_request(alice_agent.did, bob_agent.did, task_payload)
    print(f"    - Trace ID: {packet['trace_id']}")

    # 3. Bob xử lý - CHẠY TRONG claim idempotency, nên khi có retry đồng thời
    #    thì Agent B chỉ được gọi đúng một lần.
    def _do_work():
        bob_result = bob_agent.process_task(packet['task'])
        print(f"[{bob_agent.name}] Đã xử lý xong. Kết quả:")
        print(json.dumps(bob_result, indent=2, ensure_ascii=False))
        return bob_result

    receipt = bridge.execute_once(
        task_payload["operation_id"], _do_work, packet['trace_id'])

    # 4. Bridge cấp biên nhận
    print("\n[3] NAN AI2AI cấp Biên nhận Xác thực (Verification Receipt):")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))

    # 5. RETRY: ACK bị mất, Alice gửi lại CÙNG operation_id
    print(f"\n[4] {alice_agent.name} KHÔNG nhận được ACK -> gửi lại yêu cầu "
          f"với CÙNG operation_id='{task_payload['operation_id']}':")
    retry_packet = bridge.route_request(alice_agent.did, bob_agent.did, task_payload)
    print(f"    - Trace ID (mới): {retry_packet['trace_id']}")

    cached = bridge.lookup_cached_receipt(task_payload["operation_id"])
    if cached is not None:
        print("   [Bridge] Duplicate detected! Returning cached receipt.")
        print(f"    - KHÔNG gọi lại {bob_agent.name} (số lần đã thực thi: {bob_agent.calls})")
        print(f"    - Biên nhận trả lại: {cached['receipt_id']} "
              f"(trùng với lần đầu: {cached['receipt_id'] == receipt['receipt_id']})")
        receipt = cached
    else:
        print("   [Bridge] Không phát hiện trùng lặp — sẽ thực thi lại.")

    print("\n" + "=" * 70)
    print(f" HOÀN TẤT: giao dịch idempotent — {bob_agent.name} chỉ thực thi "
          f"{bob_agent.calls} lần dù Alice gửi 2 lần.")
    print("=" * 70)

if __name__ == "__main__":
    # Windows: console mac dinh dung code page cp1252 -> khong ma hoa duoc tieng Viet.
    # Chuyen stdout/stderr sang UTF-8 de demo chay duoc tren may cua nguoi dung Viet.
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except (OSError, ValueError):
                pass
    run_demo()
