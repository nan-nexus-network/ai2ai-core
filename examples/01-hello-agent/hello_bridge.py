# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""
NAN AI2AI-SI2SI: 60-Second Runnable Demo (Zero External Dependencies)
Tương thích: Python 3.8+ (Chỉ sử dụng Python Standard Library)
Giấy phép: Apache License 2.0
Chủ đề: Minh họa "Cầu nối Giao thức" (Protocol Bridge) giữa 2 Agent khác hệ sinh thái.

Lưu ý kỹ thuật (PoC Disclaimer):
- Mã nguồn này được dựng với sự hỗ trợ của AI nhằm minh họa luận điểm trong Tài liệu thảo luận.
- Hàm sanitize_and_validate hiện kiểm tra cấu trúc gói tin cơ bản và quét mẫu chuỗi tĩnh trên toàn bộ packet.
  Trong môi trường Production thực tế, tầng này cần được thay thế bằng JSON Schema Validator chuẩn,
  chữ ký số bất đối xứng (Ed25519/DID) và bộ lọc ngữ nghĩa.

Cách chạy:
python examples/01-hello-agent/hello_bridge.py
"""

import json
import uuid
import hashlib
import logging
import sys
from datetime import datetime, timezone
from typing import Tuple, Dict, List, Any, Optional

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

    @staticmethod
    def sanitize_and_validate(
        full_packet: Dict[str, Any], required_arg_fields: List[str]
    ) -> Tuple[bool, str]:
        """
        Kiểm tra toàn bộ gói tin (bao gồm cả định danh người gửi và tham số đầu vào).
        """
        # 1. Kiểm tra cấu trúc khung của gói tin gốc
        if not isinstance(full_packet, dict):
            return False, "Gói tin không phải định dạng Dictionary/JSON hợp lệ."
        if not full_packet.get("context_id") or not isinstance(full_packet.get("context_id"), str):
            return False, "Thiếu hoặc sai định dạng 'context_id' (Định danh tác tử gửi)."

        tool_call = full_packet.get("tool_call")
        if not isinstance(tool_call, dict) or not tool_call.get("name"):
            return False, "Thiếu thông tin 'tool_call.name'."

        # 2. Kiểm tra các trường bắt buộc trong arguments theo hợp đồng dữ liệu
        arguments = tool_call.get("arguments", {})
        if not isinstance(arguments, dict):
            return False, "Trường 'arguments' phải là một đối tượng JSON."

        for field in required_arg_fields:
            if field not in arguments:
                return False, f"Thiếu trường dữ liệu bắt buộc trong hợp đồng: '{field}'"

        # 3. Quét mẫu Prompt Injection trên TOÀN BỘ gói tin (kể cả context_id và tool_call)
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
    def issue_verification_receipt(
        bridged_packet: Dict[str, Any], execution_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a demo receipt with a SHA-256 digest; this does not verify identity or execution."""
        raw_record = (
            json.dumps(bridged_packet, sort_keys=True) + json.dumps(execution_output, sort_keys=True)
        )
        proof_hash = hashlib.sha256(raw_record.encode("utf-8")).hexdigest()

        return {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "trace_id": bridged_packet["trace_id"],
            "status": "DEMO_DIGEST_ONLY",
            "sha256_proof": proof_hash,
            "result_data": execution_output
        }


def run_demo() -> None:
    logger.info("%s", "=" * 74)
    logger.info("THỬ NGHIỆM 60 GIÂY: CẦU NỐI GIAO THỨC LIÊN VẬN (NAN AI2AI BRIDGE POC)")
    logger.info("%s", "=" * 74)

    # Bước 1: Agent từ Hệ sinh thái A phát tín hiệu bằng chuẩn riêng của nó
    ecosystem_a_packet = {
        "context_id": "did:eco_a:travel_assistant_01",
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
        "compliance_standard": "ASEAN_Digital_Masterplan_2030"
    }

    # Bước 4: Tạo digest demo; bước này không xác thực giao dịch hay nguồn gốc dữ liệu.
    receipt = bridge.issue_verification_receipt(bridged_packet, ecosystem_b_response)
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
