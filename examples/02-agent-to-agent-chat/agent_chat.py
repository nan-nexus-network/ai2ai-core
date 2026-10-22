# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""
NAN AI2AI-SI2SI: P2P Agent Chat Demo (Zero Dependencies)
Tương thích: Python 3.8+ (Chỉ sử dụng Python Standard Library)
Giấy phép: Apache License 2.0

Kịch bản: Alice (Agent A) muốn tìm nhà cung cấp linh kiện tại Quảng Châu.
Cô ấy gửi yêu cầu qua NAN Bridge đến Bob (Agent B) - người sở hữu dữ liệu chuỗi cung ứng.
Hai Agent tự đàm phán và Bob gửi lại kết quả kèm Biên nhận xác thực (SHA-256).

Lưu ý: Đây là mô phỏng luồng (simulation). Chữ ký số xác thực danh tính (Ed25519)
đang được phát triển tại Issue #2. Kết quả SHA-256 ở đây chỉ đảm bảo tính toàn vẹn
dữ liệu (Integrity), không xác thực danh tính hay nguồn gốc.
"""

import json
import hashlib
import uuid
import sys
from datetime import datetime, timezone

class NANBridgeNode:
    """Mô phỏng Node Cầu nối NAN AI2AI"""

    #: Cache loại trừ trùng lặp (deduplication cache) — mức PoC, trong bộ nhớ.
    #:
    #: Cùng giới hạn như `ProtocolBridgeNode._receipt_cache` trong
    #: `examples/01-hello-agent/hello_bridge.py`: mất khi khởi động lại, không
    #: dùng chung giữa các tiến trình, không có TTL. Việc hợp nhất hai hiện
    #: thực bridge còn lại nằm trong backlog (xem `ROADMAP.md`, mục BL4).
    _receipt_cache = {}

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
        entry = NANBridgeNode._receipt_cache.get(operation_id)
        return dict(entry) if entry else None

    @staticmethod
    def issue_receipt(trace_id: str, result: dict, operation_id: str) -> dict:
        """Cấp biên nhận xác thực SHA-256, có loại trừ trùng lặp theo operation_id.

        Nếu `operation_id` đã có biên nhận, trả lại biên nhận cũ kèm log
        "Duplicate detected! Returning cached receipt."
        """
        cached = NANBridgeNode.lookup_cached_receipt(operation_id)
        if cached is not None:
            print("   [Bridge] Duplicate detected! Returning cached receipt.")
            return cached
        raw_data = json.dumps(result, sort_keys=True) + trace_id
        proof = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        receipt = {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "trace_id": trace_id,
            "operation_id": operation_id,
            "status": "DIGEST_ISSUED_BY_NAN_BRIDGE",
            "sha256_proof": proof,
            "data": result
        }
        NANBridgeNode._receipt_cache[operation_id] = dict(receipt)
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
    print(f"\n[2] NAN Bridge đang định tuyến từ {alice_agent.did} -> {bob_agent.did}...")
    packet = bridge.route_request(alice_agent.did, bob_agent.did, task_payload)
    print(f"    - Trace ID: {packet['trace_id']}")

    # 3. Bob xử lý
    bob_result = bob_agent.process_task(packet['task'])
    print(f"[{bob_agent.name}] Đã xử lý xong. Kết quả:")
    print(json.dumps(bob_result, indent=2, ensure_ascii=False))

    # 4. Bridge cấp biên nhận
    print("\n[3] NAN Bridge cấp Biên nhận Xác thực (Verification Receipt):")
    receipt = bridge.issue_receipt(packet['trace_id'], bob_result, task_payload["operation_id"])
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
