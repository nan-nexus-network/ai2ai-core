# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""
NAN AI2AI-SI2SI: 60-Second Runnable Demo (Zero External Dependencies)
Tương thích: Python 3.8+ (Chỉ sử dụng Python Standard Library)
Giấy phép: Apache License 2.0
Chủ đề: Minh họa "Cầu nối Giao thức" (Protocol Bridge) giữa 2 Agent khác hệ sinh thái.

Lưu ý kỹ thuật (PoC Disclaimer):
- Mã nguồn này được dựng với sự hỗ trợ của AI nhằm minh họa luận điểm trong Tài liệu thảo luận.
- Tầng kiểm tra đã có 2 lớp (v0.2):
  Lớp 1 - kiểm tra cấu trúc theo allowlist schema (subset JSON Schema Draft 2020-12,
          tự triển khai bằng thư viện chuẩn): `nan_ai2ai/validation.py`.
          Kiểm tra kiểu dữ liệu, độ dài, miền giá trị, và TỪ CHỐI mọi trường
          không nằm trong schema.
  Lớp 2 - quét mẫu chuỗi tĩnh (blocklist) như một lớp phòng thủ thứ hai.
          CÁCH NÀY CỐ TÌNH SƠ KHAI và sẽ gây false-positive
          (ví dụ: ghi chú hàng hóa hợp pháp "drop table shipment at port" sẽ bị chặn nhầm).
          Ở bản Production, tầng này phải dùng Semantic Classifier + Allowlist Schema.
- Chữ ký số bất đối xứng (Ed25519/DID) cho biên nhận: xem `nan_ai2ai/receipt.py`
  và `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`.
- **Idempotency:** mỗi gói tin phải có `operation_id` (khoá idempotency). Cùng một
  `operation_id` sẽ chỉ được thực thi **một lần**; lần retry nhận lại đúng biên
  nhận cũ nhờ deduplication cache (`ProtocolBridgeNode._receipt_cache`).
  Đây là cơ chế **mức PoC, trong bộ nhớ tiến trình** — xem `ARCHITECTURE.md`.

Cách chạy:
python examples/01-hello-agent/hello_bridge.py
"""

import json
import uuid
import hashlib
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Tuple, Dict, List, Any, Optional

# Thêm thu muc goc kho vao sys.path de import duoc goi `nan_ai2ai`.
# Van hoat dong 100% thu vien chuan - khong dung goi cai dat nao.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from nan_ai2ai.validation import bridge_packet_schema, validate  # noqa: E402

logger = logging.getLogger(__name__)


def decode_json_packet(raw_json: str) -> Optional[Dict[str, Any]]:
    """Decode a JSON object, logging malformed or non-object input without echoing it."""
    if not isinstance(raw_json, str):
        logger.warning("Rejected JSON input because it was not text")
        return None

    try:
        packet = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        logger.warning(
            "Rejected malformed JSON input at line %d, column %d",
            exc.lineno,
            exc.colno,
        )
        return None

    if not isinstance(packet, dict):
        logger.warning("Rejected JSON input because the top-level value was not an object")
        return None

    return packet


class ProtocolBridgeNode:
    """
    Mô phỏng cục bộ việc kiểm tra một số trường, ánh xạ dữ liệu và tạo digest mẫu.
    Không kết nối hoặc xác thực các Agent ở hệ sinh thái khác nhau.
    """

    #: Cache loại trừ trùng lặp (deduplication cache), dùng để chống Replay.
    #:
    #: Mỗi ``operation_id`` ánh xạ tới một mục cache gồm biên nhận đã cấp và
    #: digest của task, để phát hiện cả trường hợp *dùng lại cùng khoá cho
    #: một task khác*.
    #:
    #: **Giới hạn PoC (cần nói rõ khi trả lời báo chí):**
    #:   - Trạng thái **chỉ tồn tại trong bộ nhớ tiến trình**: mất khi khởi
    #:     động lại, và **không** dùng chung giữa nhiều tiến trình/nút.
    #:   - **Không có TTL**: cache phình vô hạn nếu không dọn.
    #:   - Khoá là do phía gọi tự chọn, nên **người gọi phải tạo khoá khác nhau
    #:     cho mỗi thao tác logic**; dùng lại khoá cho hai thao tác khác nhau là
    #:     lỗi phía gọi (được phát hiện và ghi cảnh báo, xem
    #:     ``issue_verification_receipt``).
    _receipt_cache: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def sanitize_and_validate(
        full_packet: Dict[str, Any], required_arg_fields: List[str]
    ) -> Tuple[bool, str]:
        """
        Kiểm tra toàn bộ gói tin (bao gồm cả định danh người gửi và tham số đầu vào).

        Lớp 1: allowlist schema (kiểu dữ liệu, độ dài, miền giá trị, trường lạ).
        Lớp 2: quét mẫu chuỗi tĩnh - lớp phòng thủ thứ hai, CỐ TÌNH sơ khai.
        """
        # Lớp 0 — khoá idempotency (chống thực thi lặp / Replay).
        if not isinstance(full_packet, dict):
            return False, "Gói tin không phải định dạng Dictionary/JSON hợp lệ."
        operation_id = full_packet.get("operation_id")
        if not isinstance(operation_id, str) or not operation_id.strip():
            return False, (
                "Thiếu hoặc sai định dạng 'operation_id' (khoá idempotency: "
                "cùng một operation_id chỉ được thực thi đúng một lần)."
            )

        # Lớp 1 — kiểm tra cấu trúc theo allowlist schema.
        schema = bridge_packet_schema(required_arg_fields)
        schema_errors = validate(full_packet, schema)
        if schema_errors:
            return False, "Cấu trúc không hợp lệ: " + "; ".join(schema_errors)

        # Lớp 2 — quét mẫu Prompt Injection trên TOÀN BỘ gói tin.
        # LƯU Ý KỸ THUẬT (PoC Limitation):
        # Pattern matching bằng danh sách từ khóa cấm (blocklist) ở đây cố tình làm tối giản
        # để minh họa luồng chặn của Cầu nối. Trong thực tế, cách này sẽ gây false-positive
        # (ví dụ: ghi chú hàng hóa hợp pháp "drop table shipment at port" sẽ bị chặn nhầm vì chứa "drop table").
        # Ở bản Production, tầng này phải dùng Semantic Classifier + Allowlist Schema thay vì Blocklist tĩnh.
        raw_full_text = json.dumps(full_packet, ensure_ascii=False).lower()
        forbidden_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "system override",
            "drop table",
            "<script>"
        ]
        for pattern in forbidden_patterns:
            if pattern in raw_full_text:
                return False, f"Cảnh báo an toàn (PoC Rule): Phát hiện mẫu chuỗi đáng ngờ ('{pattern}')"

        return True, "Hợp lệ"

    @staticmethod
    def translate_mcp_to_a2a(mcp_message: Dict[str, Any]) -> Dict[str, Any]:
        """Chuyển đổi ngữ nghĩa gói tin từ chuẩn Hệ sinh thái A sang chuẩn Liên vận Hệ sinh thái B."""
        return {
            "bridge_protocol": "NAN-AI2AI-Bridge/v0.1-poc",
            "trace_id": f"vn_bridge_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ecosystem": "Ecosystem_A (MCP-Style)",
            "target_ecosystem": "Ecosystem_B (A2A-Style)",
            "standardized_task": {
                "action": mcp_message["tool_call"]["name"],
                "parameters": mcp_message["tool_call"].get("arguments", {}),
                "caller_identity": mcp_message["context_id"]
            }
        }

    @staticmethod
    def lookup_cached_receipt(operation_id: str) -> Optional[Dict[str, Any]]:
        """Trả về biên nhận đã cấp cho ``operation_id``, hoặc ``None``.

        Dùng để kiểm tra **trước khi** gọi bên thực thi, để một lần retry không
        làm tác vụ chạy hai lần.
        """
        if not isinstance(operation_id, str) or not operation_id:
            return None
        entry = ProtocolBridgeNode._receipt_cache.get(operation_id)
        if entry is None:
            return None
        return dict(entry["receipt"])

    @staticmethod
    def issue_verification_receipt(
        bridged_packet: Dict[str, Any],
        execution_output: Dict[str, Any],
        operation_id: str,
    ) -> Dict[str, Any]:
        """Create a demo receipt with a SHA-256 digest; this does not verify identity or execution.

        ``operation_id`` là khoá idempotency. Nếu khoá này đã được cấp biên nhận
        trước đó, hàm **không tạo biên nhận mới** mà trả lại biên nhận đã lưu,
        kèm log ``Duplicate detected! Returning cached receipt.``
        """
        if not isinstance(operation_id, str) or not operation_id.strip():
            raise ValueError(
                "operation_id khong duoc rong: can khoa idempotency de chong "
                "thuc thi lap (replay).")

        cached = ProtocolBridgeNode.lookup_cached_receipt(operation_id)
        if cached is not None:
            logger.warning("Duplicate detected! Returning cached receipt.")
            return cached

        raw_record = (
            json.dumps(bridged_packet, sort_keys=True) + json.dumps(execution_output, sort_keys=True)
        )
        proof_hash = hashlib.sha256(raw_record.encode("utf-8")).hexdigest()

        receipt = {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "trace_id": bridged_packet["trace_id"],
            "operation_id": operation_id,
            "status": "DEMO_DIGEST_ONLY",
            "sha256_proof": proof_hash,
            "result_data": execution_output
        }

        # Luu vao cache de lan retry nhan duoc cung mot bien nhan.
        task_digest = hashlib.sha256(
            json.dumps(bridged_packet.get("standardized_task", {}), sort_keys=True).encode("utf-8")
        ).hexdigest()
        ProtocolBridgeNode._receipt_cache[operation_id] = {
            "receipt": dict(receipt),
            "task_digest": task_digest,
        }
        return receipt


def run_demo() -> None:
    logger.info("%s", "=" * 74)
    logger.info("THỬ NGHIỆM 60 GIÂY: CẦU NỐI GIAO THỨC LIÊN VẬN (NAN AI2AI BRIDGE POC)")
    logger.info("%s", "=" * 74)

    # Bước 1: Agent từ Hệ sinh thái A phát tín hiệu bằng chuẩn riêng của nó
    ecosystem_a_packet = {
        "context_id": "did:eco_a:travel_assistant_01",
        "operation_id": "op_demo_0001",
        "tool_call": {
            "name": "query_asean_logistics_slot",
            "arguments": {
                "route": "DaNang_to_Singapore",
                "cargo_type": "Electronics",
                "max_latency_hours": 24
            }
        }
    }
    logger.info("[1] Gói tin mẫu từ Agent Hệ sinh thái A (MCP-style):")
    decoded_packet = decode_json_packet(json.dumps(ecosystem_a_packet, ensure_ascii=False))
    if decoded_packet is None:
        logger.error("Demo stopped because the sample packet could not be decoded")
        return
    logger.info("%s", json.dumps(decoded_packet, indent=2, ensure_ascii=False))

    # Bước 2: Qua Cầu nối NAN AI2AI kiểm tra toàn bộ packet & dịch chuẩn
    bridge = ProtocolBridgeNode()
    is_valid, validation_msg = bridge.sanitize_and_validate(
        full_packet=decoded_packet, required_arg_fields=["route", "cargo_type"]
    )
    if not is_valid:
        logger.warning("Cầu nối từ chối gói tin mẫu: %s", validation_msg)
        return

    bridged_packet = bridge.translate_mcp_to_a2a(decoded_packet)
    logger.info("[2] Gói tin sau kiểm tra cấu trúc PoC và chuyển đổi:")
    logger.info("%s", json.dumps(bridged_packet, indent=2, ensure_ascii=False))

    # Bước 3: Agent từ Hệ sinh thái B nhận việc và trả kết quả
    ecosystem_b_response = {
        "provider_did": "did:eco_b:asean_freight_node_09",
        "slot_available": True,
        "estimated_hours": 18,
        "compliance_standard": "ASEAN_Digital_Masterplan_2026_2030"
    }

    # Bước 4: Tạo digest demo; bước này không xác thực giao dịch hay nguồn gốc dữ liệu.
    receipt = bridge.issue_verification_receipt(
        bridged_packet, ecosystem_b_response, decoded_packet["operation_id"]
    )
    logger.info("[3] Biên nhận demo có mã băm SHA-256 (không xác thực nguồn gốc):")
    logger.info("%s", json.dumps(receipt, indent=2, ensure_ascii=False))

    logger.info("%s", "=" * 74)
    logger.info("HOÀN TẤT DEMO CỤC BỘ: dữ liệu mẫu và phản hồi mô phỏng đã đi qua các hàm PoC.")
    logger.info("Tài liệu thảo luận: docs/WHITEPAPER_VN_AI_BRIDGE.md")
    logger.info("%s", "=" * 74)


if __name__ == "__main__":
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (OSError, ValueError):
            pass
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run_demo()
