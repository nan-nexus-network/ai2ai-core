# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""NAN AI2AI-SI2SI: Bien nhan xac thuc co chu ky (Signed Receipt Demo).

Chay:
    python examples/03-signed-receipt/signed_receipt_demo.py

Demo nay tra loi mot cau hoi duy nhat: **ben thu ba xac minh duoc mot bien
nhan ma KHONG CAN TIN VAO BRIDGE khong?**

Ke thich:
    Alice (caller) ---> NAN Bridge ---> Bob (executor)
                          |                    |
                          |              ky bien nhan bang khoa rieng
                          |                    |
                          v                    v
                    nhan "transporter    <-- CHUNG MINH duoc
                    attestation"          boi bat ky ai giu khoa
                                           cua Bob

Ghi chu trung thuc
------------------
* Chữ ký ở đây dùng **Ed25519 thuần Python** (RFC 8032), chỉ để giữ cam kết
  "Zero Dependencies". Xem ``nan_ai2ai/ed25519.py`` cho cảnh báo an toàn.
* Mô hình neo tin cậy là **TOFU** (ghim khoá lần đầu). Nó **không** bảo vệ
  được lần tiếp xúc đầu tiên. Xem ``nan_ai2ai/trust.py``.
* Biên nhận **không** thay thế hợp đồng, không có giá trị pháp lý, và
  **không** phải tiêu chuẩn hoá. Đây là PoC trong một Open Reference Framework.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from nan_ai2ai import canonical, ed25519, receipt, trust  # noqa: E402


def _log(step: str, message: str) -> None:
    print("  %-58s %s" % (message, step))


def main() -> int:
    print("=" * 78)
    print(" NAN AI2AI: SIGNED VERIFICATION RECEIPT DEMO (nan-receipt/v1)")
    print("=" * 78)

    now = datetime.now(timezone.utc)

    print("\n[1] Executor (Bob) chuan bi cap khoa Ed25519:")
    bob_secret, bob_public = ed25519.generate_keypair()
    bob_kid = receipt.jwk_thumbprint(bob_public)
    print("      kid (JWK thumbprint RFC 7638): %s" % bob_kid)
    _log("", "khoa cong khai KHONG duoc dua vao bien nhan - chi co 'kid'")

    print("\n[2] Agent Card cua Bob (tuong thich hinh dang A2A, khong phai ban A2A):")
    card = trust.agent_card(
        agent_id="did:nan:bob_02",
        public_key=bob_public,
        capabilities={"streaming": False, "pushNotifications": False},
        endpoint="",
        skills=[{"id": "query_asean_logistics_slot", "name": "Tra cua hang hoa"}],
    )
    print("      name=%s | skills=%d | kid=%s" % (
        card["name"], len(card["skills"]), card["kid"]))
    _log("", "The moi chua ky: card CHUA co 'signatures' -> chua co neo tin cay")

    print("\n[3] Alice tao task, Bob tra ket qua:")
    task = {
        "action": "query_asean_logistics_slot",
        "parameters": {"route": "DaNang_to_Singapore", "cargo_type": "Electronics"},
    }
    result = {"status": "success", "slot_available": True, "estimated_hours": 18}
    print("      task  : %s" % canonical.canonical_json(task).decode())
    print("      result: %s" % canonical.canonical_json(result).decode())

    print("\n[4] Bob (executor) tao bien nhan va KY:")
    draft = receipt.build_receipt(
        trace_id="trace_demo_0001",
        task=task,
        result=result,
        executor_agent_id="did:nan:bob_02",
        executor_public_key=bob_public,
        issued_at=now.isoformat().replace("+00:00", "Z"),
        expires_at=(now + timedelta(minutes=15)).isoformat().replace("+00:00", "Z"),
    )
    signed = receipt.sign_receipt(draft, bob_secret)
    print("      receipt_id  : %s" % signed["receipt_id"])
    print("      nonce       : %s" % signed["nonce"])
    print("      expires_at  : %s" % signed["expires_at"])
    print("      task_digest : %s" % signed["subject"]["task_digest"][:32] + "...")
    print("      result_dig  : %s" % signed["subject"]["result_digest"][:32] + "...")
    print("      signatures  : %d (role=%s, alg=%s)" % (
        len(signed["signatures"]),
        signed["signatures"][0]["role"], signed["signatures"][0]["alg"]))
    _log("", "chi EXECUTOR ky. Bridge khong co quyen ky o truong nay.")

    print("\n[5] Bridge them 'transporter attestation' (khong mang gi tri chung minh):")
    bridge_secret, bridge_public = ed25519.generate_keypair()
    bridge_payload = canonical.digest_input(
        canonical.DOMAIN_SIGNATURE + "/transporter",
        canonical.canonical_json({
            "trace_id": signed["trace_id"],
            "receipt_id": signed["receipt_id"],
        }),
    )
    attested = receipt.add_transporter_attestation(
        signed,
        transporter_id="nan-bridge-node-01",
        signature=ed25519.sign(bridge_secret, bridge_payload),
        kid=receipt.jwk_thumbprint(bridge_public),
    )
    entry = attested["transporter_attestations"][0]
    print("      transporter_id      : %s" % entry["transporter_id"])
    print("      evidentiary_weight  : %s" % entry["evidentiary_weight"])
    _log("", "ben xac minh KHONG dung truong nay de quyet dinh hop le hay khong")

    print("\n[6] Ben thu ba xac minh - KHONG CO QUYEN TRU BOI BRIDGE:")
    store = trust.TrustStore()
    print("      trust store luc dau: %d khoa da ghim" % len(store))
    first_contact = store.pin(bob_kid, bob_public)
    print("      ghim TOFU lan dau  : %s" % ("da ghim" if first_contact else "da co san"))
    report = trust.verify_with_store(attested, store, task=task, result=result)
    print("      ket qua            : %s" % report.summary())
    for check in report.checks:
        print("         - %s" % check)

    print("\n[7] Kiem tra phu dinh (tam chien, het han, xung dot khoa):")

    tampered = dict(attested)
    tampered["result_digest"] = "0" * 64
    r1 = receipt.verify_receipt(tampered, {bob_kid: bob_public}, task=task, result=result)
    print("      ket qua doi ket qua : %s" % r1.summary())

    expired = receipt.build_receipt(
        trace_id="trace_demo_0002", task=task, result=result,
        executor_agent_id="did:nan:bob_02", executor_public_key=bob_public,
        issued_at=(now - timedelta(hours=2)).isoformat().replace("+00:00", "Z"),
        expires_at=(now - timedelta(hours=1)).isoformat().replace("+00:00", "Z"),
    )
    expired_signed = receipt.sign_receipt(expired, bob_secret)
    r2 = receipt.verify_receipt(expired_signed, {bob_kid: bob_public})
    print("      bien nhan het han    : %s" % r2.summary())

    other_secret, other_public = ed25519.generate_keypair()
    conflict_store = trust.TrustStore()
    conflict_store.pin(bob_kid, bob_public)
    try:
        conflict_store.pin(bob_kid, other_public)
        print("      xung dot khoa       : KHONG phat hien - LOI")
    except trust.TrustConflictError as exc:
        print("      xung dot khoa       : da chan - %s" % str(exc)[:70])

    print("\n" + "=" * 78)
    print(" KET LUAN: bien nhan co the duoc xac minh boi BEN THU BA chi voi")
    print("   - khoa cong khai da ghim (TOFU)")
    print("   - chu ky cua ben thuc thi")
    print("   - KHONG can tin vao Bridge, va KHONG can mot registry tap trung.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except (OSError, ValueError):
                pass
    sys.exit(main())
