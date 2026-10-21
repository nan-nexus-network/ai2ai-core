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
import sys
from datetime import datetime, timezone
from typing import Tuple, Dict, List, Any

# Hỗ trợ hiển thị tiếng Việt UTF-8 chuẩn xác trên mọi console (Windows cp1252/cp437, Linux, macOS)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ProtocolBridgeNode:
    """
    Mô phỏng Node Cầu nối (Bridge) trung lập:
    Giúp Agent Hệ sinh thái A (kiểu MCP/Tool-centric) và Agent Hệ sinh thái B (kiểu A2A/Task-centric)
    kiểm tra hợp đồng dữ liệu, lọc mẫu câu lệnh nguy hiểm và cấp biên nhận thực thi (Receipt).
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
        """
        Tạo biên nhận kiểm chứng (Verification Receipt) bằng mã băm SHA-256.
        Lưu ý: SHA-256 đảm bảo tính toàn vẹn (Integrity), cần bổ sung chữ ký số Ed25519
        ở bản tiếp theo để đảm bảo tính chống chối bỏ danh tính (Non-repudiation).
        """
        raw_record = (
            json.dumps(bridged_packet, sort_keys=True) + json.dumps(execution_output, sort_keys=True)
        )
        proof_hash = hashlib.sha256(raw_record.encode("utf-8")).hexdigest()

        return {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "trace_id": bridged_packet["trace_id"],
            "status": "VERIFIED_BY_NEUTRAL_BRIDGE",
            "sha256_proof": proof_hash,
            "result_data": execution_output
        }


def run_demo() -> None:
    print("=" * 74)
    print("   THỬ NGHIỆM 60 GIÂY: CẦU NỐI GIAO THỨC LIÊN VẬN (NAN AI2AI BRIDGE POC)")
    print("=" * 74)

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
    print("\n[1] Gói tin gốc từ Agent Hệ sinh thái A (Chuẩn MCP-Style):")
    print(json.dumps(ecosystem_a_packet, indent=2, ensure_ascii=False))

    # Bước 2: Qua Cầu nối NAN AI2AI kiểm tra toàn bộ packet & dịch chuẩn
    bridge = ProtocolBridgeNode()
    is_valid, validation_msg = bridge.sanitize_and_validate(
        full_packet=ecosystem_a_packet, required_arg_fields=["route", "cargo_type"]
    )
    if not is_valid:
        print(f"\n[!] Cầu nối từ chối gói tin: {validation_msg}")
        return

    bridged_packet = bridge.translate_mcp_to_a2a(ecosystem_a_packet)
    print("\n[2] Cầu nối đã kiểm tra toàn gói tin & chuyển đổi sang chuẩn Liên vận:")
    print(json.dumps(bridged_packet, indent=2, ensure_ascii=False))

    # Bước 3: Agent từ Hệ sinh thái B nhận việc và trả kết quả
    ecosystem_b_response = {
        "provider_did": "did:eco_b:asean_freight_node_09",
        "slot_available": True,
        "estimated_hours": 18,
        "compliance_standard": "ASEAN_Digital_Masterplan_2030"
    }

    # Bước 4: Cầu nối cấp biên nhận xác thực (Verification Receipt)
    receipt = bridge.issue_verification_receipt(bridged_packet, ecosystem_b_response)
    print("\n[3] Biên nhận hoàn tất giao dịch AI2AI (Có mã băm SHA-256 kiểm chứng):")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))

    print("\n" + "=" * 74)
    print("   HOÀN TẤT: Hai Agent khác hệ sinh thái đã phối hợp thành công qua Cầu nối.")
    print("   Đọc tài liệu thảo luận & phản biện tại: docs/WHITEPAPER_VN_AI_BRIDGE.md")
    print("=" * 74)


if __name__ == "__main__":
    run_demo()
