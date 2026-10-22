# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Kiem thu bien nhan co chu ky ``nan-receipt/v1`` va mo hinh neo tin cay.

Cau hoi trong tam can duoc chung minh bang may:
    **Ben thu ba xac minh duoc bien nhan ma KHONG CAN TIN VAO BRIDGE khong?**
"""

import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nan_ai2ai import ed25519, receipt, trust  # noqa: E402


TASK = {"action": "query_slot", "parameters": {"route": "A_to_B", "cargo_type": "X"}}
RESULT = {"status": "success", "slot_available": True}


def now_iso(offset_minutes=0):
    moment = datetime.now(timezone.utc) + timedelta(minutes=offset_minutes)
    return moment.isoformat().replace("+00:00", "Z")


class ReceiptTestBase(unittest.TestCase):

    def setUp(self):
        self.secret, self.public = ed25519.generate_keypair()
        self.kid = receipt.jwk_thumbprint(self.public)
        self.draft = receipt.build_receipt(
            trace_id="trace_test_01",
            task=TASK,
            result=RESULT,
            executor_agent_id="did:nan:bob_02",
            executor_public_key=self.public,
            issued_at=now_iso(-1),
            expires_at=now_iso(15),
        )
        self.signed = receipt.sign_receipt(self.draft, self.secret)


class TestStructure(ReceiptTestBase):

    def test_required_fields_present(self):
        for field in ("receipt_version", "receipt_id", "trace_id", "issued_at",
                      "expires_at", "nonce", "subject", "parties", "signatures"):
            self.assertIn(field, self.signed)

    def test_version_is_explicit(self):
        self.assertEqual(self.signed["receipt_version"], "nan-receipt/v1")

    def test_nonce_is_present_and_unique(self):
        self.assertTrue(self.signed["nonce"])
        other = receipt.build_receipt(
            trace_id="t", task=TASK, result=RESULT,
            executor_agent_id="a", executor_public_key=self.public,
            issued_at=now_iso(), expires_at=now_iso(5))
        self.assertNotEqual(self.signed["nonce"], other["nonce"])

    def test_digests_present_and_different(self):
        subject = self.signed["subject"]
        self.assertNotEqual(subject["task_digest"], subject["result_digest"])
        self.assertEqual(len(subject["task_digest"]), 64)

    def test_public_key_not_embedded_in_receipt(self):
        """Chi 'kid' duoc mang - khoa cong khai phai den tu nguoi ghim."""
        self.assertNotIn(self.public.hex(), str(self.signed))

    def test_kid_is_jwk_thumbprint(self):
        self.assertEqual(self.signed["parties"]["executor"]["kid"], self.kid)

    def test_signing_payload_excludes_signatures(self):
        payload = receipt.signing_payload(self.signed)
        self.assertNotIn(self.signed["signatures"][0]["sig"].encode(),
                         payload)


class TestSigningScope(ReceiptTestBase):
    """Quyet dinh: CHI executor ky. Bridge chi duoc 'ghi nhan'."""

    def test_only_executor_may_sign(self):
        with self.assertRaises(ValueError):
            receipt.sign_receipt(self.draft, self.secret, role="bridge")

    def test_executor_signature_present(self):
        roles = [s["role"] for s in self.signed["signatures"]]
        self.assertEqual(roles, ["executor"])

    def test_transporter_attestation_is_separate_field(self):
        self.assertNotIn("transporter_attestations", self.signed)
        bridge_secret, bridge_public = ed25519.generate_keypair()
        attested = receipt.add_transporter_attestation(
            self.signed, transporter_id="bridge-01",
            signature=ed25519.sign(bridge_secret, b"x"),
            kid=receipt.jwk_thumbprint(bridge_public))
        self.assertIn("transporter_attestations", attested)
        entry = attested["transporter_attestations"][0]
        self.assertEqual(entry["evidentiary_weight"], "none")

    def test_transporter_attestation_does_not_affect_verification(self):
        bridge_secret, bridge_public = ed25519.generate_keypair()
        attested = receipt.add_transporter_attestation(
            self.signed, transporter_id="bridge-01",
            signature=ed25519.sign(bridge_secret, b"x"),
            kid=receipt.jwk_thumbprint(bridge_public))
        plain = receipt.verify_receipt(self.signed, {self.kid: self.public},
                                       task=TASK, result=RESULT)
        with_bridge = receipt.verify_receipt(attested, {self.kid: self.public},
                                             task=TASK, result=RESULT)
        self.assertTrue(plain.ok)
        self.assertTrue(with_bridge.ok)


class TestVerification(ReceiptTestBase):

    def test_valid_receipt_passes(self):
        report = receipt.verify_receipt(self.signed, {self.kid: self.public},
                                        task=TASK, result=RESULT)
        self.assertTrue(report.ok, report.summary())
        self.assertIn("chu ky executor", report.checks)

    def test_missing_key_is_rejected(self):
        report = receipt.verify_receipt(self.signed, {}, task=TASK, result=RESULT)
        self.assertFalse(report.ok)

    def test_wrong_key_is_rejected(self):
        _, other_public = ed25519.generate_keypair()
        report = receipt.verify_receipt(self.signed, {self.kid: other_public},
                                        task=TASK, result=RESULT)
        self.assertFalse(report.ok)

    def test_tampered_result_digest_is_rejected(self):
        tampered = dict(self.signed)
        tampered["subject"] = dict(self.signed["subject"])
        tampered["subject"]["result_digest"] = "0" * 64
        report = receipt.verify_receipt(tampered, {self.kid: self.public},
                                        task=TASK, result=RESULT)
        self.assertFalse(report.ok)

    def test_tampered_result_content_is_rejected(self):
        report = receipt.verify_receipt(self.signed, {self.kid: self.public},
                                        task=TASK,
                                        result={"status": "success",
                                                "slot_available": False})
        self.assertFalse(report.ok)
        self.assertTrue(any("result digest" in e for e in report.errors))

    def test_expired_receipt_is_rejected(self):
        expired = receipt.build_receipt(
            trace_id="t", task=TASK, result=RESULT,
            executor_agent_id="a", executor_public_key=self.public,
            issued_at=now_iso(-120), expires_at=now_iso(-60))
        signed = receipt.sign_receipt(expired, self.secret)
        report = receipt.verify_receipt(signed, {self.kid: self.public})
        self.assertFalse(report.ok)
        self.assertTrue(any("han dung" in e for e in report.errors))

    def test_replay_window_is_enforced_by_now_parameter(self):
        report = receipt.verify_receipt(self.signed, {self.kid: self.public},
                                        now=now_iso(60))
        self.assertFalse(report.ok)

    def test_unknown_version_is_rejected(self):
        broken = dict(self.signed)
        broken["receipt_version"] = "nan-receipt/v99"
        report = receipt.verify_receipt(broken, {self.kid: self.public})
        self.assertFalse(report.ok)

    def test_missing_signature_is_rejected(self):
        broken = dict(self.signed)
        broken["signatures"] = []
        report = receipt.verify_receipt(broken, {self.kid: self.public})
        self.assertFalse(report.ok)

    def test_error_message_lists_checks(self):
        report = receipt.verify_receipt(self.signed, {}, task=TASK, result=RESULT)
        self.assertIn("KHONG HOP LE", report.summary())


class TestTrustStore(unittest.TestCase):

    def setUp(self):
        self.secret, self.public = ed25519.generate_keypair()
        self.kid = receipt.jwk_thumbprint(self.public)

    def test_first_pin_is_recorded(self):
        store = trust.TrustStore()
        self.assertTrue(store.pin(self.kid, self.public))
        self.assertEqual(len(store), 1)

    def test_second_pin_same_key_is_noop(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        self.assertFalse(store.pin(self.kid, self.public))

    def test_conflicting_key_raises(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        _, other_public = ed25519.generate_keypair()
        with self.assertRaises(trust.TrustConflictError):
            store.pin(self.kid, other_public)

    def test_check_reports_mismatch(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        _, other_public = ed25519.generate_keypair()
        self.assertFalse(store.check(self.kid, other_public))
        self.assertTrue(store.check(self.kid, self.public))

    def test_pins_returns_copy(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        copy = store.pins()
        copy["x"] = b"y"
        self.assertEqual(len(store), 1)


class TestThirdPartyVerification(unittest.TestCase):
    """Cau hoi trong tam: KHONG CAN TIN VAO BRIDGE."""

    def setUp(self):
        self.secret, self.public = ed25519.generate_keypair()
        self.kid = receipt.jwk_thumbprint(self.public)
        draft = receipt.build_receipt(
            trace_id="trace_3p", task=TASK, result=RESULT,
            executor_agent_id="did:nan:bob_02",
            executor_public_key=self.public,
            issued_at=now_iso(-1), expires_at=now_iso(15))
        self.signed = receipt.sign_receipt(draft, self.secret)

    def test_verifier_needs_only_pinned_key(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        report = trust.verify_with_store(self.signed, store, task=TASK, result=RESULT)
        self.assertTrue(report.ok, report.summary())

    def test_verifier_rejects_receipt_for_unpinned_agent(self):
        store = trust.TrustStore()
        report = trust.verify_with_store(self.signed, store, task=TASK, result=RESULT)
        self.assertFalse(report.ok)

    def test_bridge_cannot_forge_a_receipt(self):
        """Bridge gia mao bien nhan bang khoa cua chinh no -> bi tu choi."""
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        _, bridge_public = ed25519.generate_keypair()
        forged = dict(self.signed)
        forged["signatures"] = [{
            "role": "executor",
            "alg": "Ed25519",
            "kid": receipt.jwk_thumbprint(bridge_public),
            "sig": "A" * 86,
        }]
        report = trust.verify_with_store(forged, store, task=TASK, result=RESULT)
        self.assertFalse(report.ok)

    def test_bridge_cannot_alter_result_without_executor_key(self):
        store = trust.TrustStore()
        store.pin(self.kid, self.public)
        altered = dict(self.signed)
        altered["result_digest"] = "1" * 64
        report = trust.verify_with_store(altered, store, task=TASK, result=RESULT)
        self.assertFalse(report.ok)


class TestOperationId(unittest.TestCase):
    """operation_id phai nam trong payload duoc ky de khong the doi ma
    ma khong lam vo chu ky."""

    def setUp(self):
        self.secret, self.public = ed25519.generate_keypair()
        self.kid = receipt.jwk_thumbprint(self.public)
        self.draft = receipt.build_receipt(
            trace_id="trace_op", task=TASK, result=RESULT,
            executor_agent_id="did:nan:bob_02",
            executor_public_key=self.public,
            issued_at=now_iso(-1), expires_at=now_iso(15),
            operation_id="op_123456")

    def test_operation_id_is_present(self):
        self.assertEqual(self.draft["operation_id"], "op_123456")

    def test_operation_id_is_covered_by_the_signature(self):
        signed = receipt.sign_receipt(self.draft, self.secret)
        payload = receipt.signing_payload(signed)
        self.assertIn(b"op_123456", payload)

    def test_tampering_with_operation_id_breaks_the_signature(self):
        signed = receipt.sign_receipt(self.draft, self.secret)
        tampered = dict(signed)
        tampered["operation_id"] = "op_999999"
        report = receipt.verify_receipt(tampered, {self.kid: self.public})
        self.assertFalse(report.ok)

    def test_verification_still_passes(self):
        signed = receipt.sign_receipt(self.draft, self.secret)
        report = receipt.verify_receipt(signed, {self.kid: self.public},
                                       task=TASK, result=RESULT)
        self.assertTrue(report.ok, report.summary())

    def test_empty_operation_id_is_rejected(self):
        with self.assertRaises(ValueError):
            receipt.build_receipt(
                trace_id="t", task=TASK, result=RESULT,
                executor_agent_id="a", executor_public_key=self.public,
                issued_at=now_iso(), expires_at=now_iso(5),
                operation_id="   ")

    def test_operation_id_is_optional(self):
        without = receipt.build_receipt(
            trace_id="t", task=TASK, result=RESULT,
            executor_agent_id="a", executor_public_key=self.public,
            issued_at=now_iso(), expires_at=now_iso(5))
        self.assertNotIn("operation_id", without)


class TestAgentCard(unittest.TestCase):

    def setUp(self):
        self.secret, self.public = ed25519.generate_keypair()

    def test_card_contains_kid_and_jwk(self):
        card = trust.agent_card(agent_id="did:nan:bob_02", public_key=self.public)
        self.assertEqual(card["kid"], receipt.jwk_thumbprint(self.public))
        self.assertEqual(card["publicKeyJwk"]["crv"], "Ed25519")
        self.assertEqual(card["publicKeyJwk"]["kty"], "OKP")

    def test_card_has_a2a_aligned_field_names(self):
        card = trust.agent_card(agent_id="did:nan:bob_02", public_key=self.public)
        for field in ("name", "version", "provider", "capabilities", "skills",
                      "supportedInterfaces", "signatures", "securityRequirements"):
            self.assertIn(field, card)

    def test_card_is_deterministic(self):
        a = trust.agent_card(agent_id="x", public_key=self.public)
        b = trust.agent_card(agent_id="x", public_key=self.public)
        self.assertEqual(trust.card_to_json(a), trust.card_to_json(b))

    def test_did_is_optional(self):
        without = trust.agent_card(agent_id="x", public_key=self.public)
        with_did = trust.agent_card(agent_id="x", public_key=self.public,
                                    did="did:web:example.com")
        self.assertNotIn("did", without)
        self.assertEqual(with_did["did"], "did:web:example.com")


if __name__ == "__main__":
    unittest.main()
