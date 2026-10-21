# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Bien nhan xac thuc co chu ky: ``nan-receipt/v1``.

Quyet dinh thiet ke (xem ``docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md``)
---------------------------------------------------------------------------
**Ben thuc thi ky. Bridge khong bat buoc ky.**

Ly do: neu Bridge ky thi ben thu ba xac minh phai quyet dinh co "tin Bridge"
khong. Neu chi executor ky, thi:
  - Bridge **khong the** gia mao bien nhan (khong co khoa executor);
  - Bridge **khong the** sua ket qua (``result_digest`` nam trong pham vi chu ky);
  - ben thu ba xac minh duoc **ma khong can tin vao bat ky ben nao khac**
    ngoai ca nguoi ky.

Vi vay ``signatures`` chi chua chu ky cua **executor** (bat buoc). Neu muon
ghi nhan "Bridge da thay gi", dung truong rieng ``transporter_attestations`` -
no **khong mang gi tri chung minh** va khong bao gio duoc dung de quyet dinh
"co hop le hay khong".

Moi truong trong bien nhan deu duoc chuan hoa truoc khi bam/chu ky, va moi
phan deu co **do dai dai truoc** + **domain separator** (xem
``nan_ai2ai.canonical``), nen khong con lo "hai blob JSON noi truc tiep".
"""

from __future__ import annotations

import base64
import hashlib
import os
from typing import Any, Dict, List, Mapping, Optional, Sequence

from . import canonical, ed25519

__all__ = [
    "RECEIPT_VERSION",
    "VerificationReport",
    "build_receipt",
    "compute_digests",
    "jwk_thumbprint",
    "sign_receipt",
    "signing_payload",
    "verify_receipt",
]


RECEIPT_VERSION = "nan-receipt/v1"

#: Cac truong khong duoc nam trong payload duoc ky (chu ky luon tinh rieng).
_UNSIGNED_FIELDS = ("signatures", "transporter_attestations")


def _b64u(data: bytes) -> str:
    """base64url khong padding (JWS JWK convention, RFC 7515)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64u(text: str) -> bytes:
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def jwk_thumbprint(public_key: bytes) -> str:
    """Thumbprint JWK (RFC 7638) cua khoa cong khai Ed25519, dang base64url.

    JWK Ed25519 chi co 3 thanh phan bat buoc: ``crv``, ``kty``, ``x``.
    RFC 7638 yeu cau JSON khong khoang trang, chi dung cac thanh phan bat buoc,
    va khoa sap xep theo thu tu tu dien.

    Dung ``kid`` = thumbprint de dinh danh khoa **khong can registry** - xem
    ``nan_ai2ai.trust``.
    """
    if len(public_key) != 32:
        raise ValueError("Khoa cong khai Ed25519 phai dai 32 byte")
    jwk = {"crv": "Ed25519", "kty": "OKP", "x": _b64u(public_key)}
    thumb_input = canonical.canonical_json(jwk)  # sort_keys=True -> crv, kty, x
    return _b64u(hashlib.sha256(thumb_input).digest())


def compute_digests(task: Any, result: Any) -> Dict[str, str]:
    """Tinh ``task_digest`` va ``result_digest`` (SHA-256 hex, co domain rieng).

    Hai digest dùng **domain separator khac nhau** de mot digest khong the
    "di hoc" sang vai tro khac.
    """
    return {
        "task_digest": canonical.digest_of(
            canonical.DOMAIN_RECEIPT, canonical.canonical_json(task)),
        "result_digest": canonical.digest_of(
            canonical.DOMAIN_RECEIPT + "/result", canonical.canonical_json(result)),
    }


def build_receipt(
    *,
    trace_id: str,
    task: Any,
    result: Any,
    executor_agent_id: str,
    executor_public_key: bytes,
    issued_at: str,
    expires_at: str,
    nonce: Optional[str] = None,
) -> Dict[str, Any]:
    """Tao bien nhan **chua ky** (trang thai "awaiting signature").

    ``nonce`` mac dinh la 16 byte ngau nhien. ``expires_at`` la moc het han
    (chong replay) - ben xac minh se tu choi bien nhan da het han.
    """
    if not trace_id:
        raise ValueError("trace_id khong duoc rong")
    if not executor_agent_id:
        raise ValueError("executor_agent_id khong duoc rong")
    if nonce is None:
        nonce = _b64u(os.urandom(16))
    digests = compute_digests(task, result)
    kid = jwk_thumbprint(executor_public_key)
    return {
        "receipt_version": RECEIPT_VERSION,
        "receipt_id": "rcpt_" + _b64u(os.urandom(10)),
        "trace_id": trace_id,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "nonce": nonce,
        "subject": digests,
        "parties": {
            "caller": {"agent_id": "", "kid": ""},
            "executor": {"agent_id": executor_agent_id, "kid": kid},
        },
        "signatures": [],
    }


def signing_payload(receipt: Mapping[str, Any]) -> bytes:
    """Payload byte duoc ky.

    = ``digest_input(DOMAIN_SIGNATURE, canonical_json(receipt truong ky))``

    Bi loai ``signatures`` va ``transporter_attestations`` khoi no dung.
    """
    body = {k: v for k, v in receipt.items() if k not in _UNSIGNED_FIELDS}
    return canonical.digest_input(
        canonical.DOMAIN_SIGNATURE, canonical.canonical_json(body))


def sign_receipt(
    receipt: Mapping[str, Any],
    secret_key: bytes,
    *,
    role: str = "executor",
) -> Dict[str, Any]:
    """Ky bien nhan bang khoa bi mat va tra ve **ban sao moi** co ``signatures``.

    ``role`` phai la ``"executor"``. Khong cung cap ``"bridge"`` o day co y:
    xem ``add_transporter_attestation``.
    """
    if role != "executor":
        raise ValueError(
            "Chi 'executor' duoc ky trong truong 'signatures'. "
            "Bridge chi duoc ghi nhan o 'transporter_attestations'.")
    signature = ed25519.sign(secret_key, signing_payload(receipt))
    signed = dict(receipt)
    signed["signatures"] = list(receipt.get("signatures", [])) + [{
        "role": "executor",
        "alg": "Ed25519",
        "kid": receipt["parties"]["executor"]["kid"],
        "sig": _b64u(signature),
    }]
    return signed


def add_transporter_attestation(
    receipt: Mapping[str, Any],
    *,
    transporter_id: str,
    signature: bytes,
    kid: str,
) -> Dict[str, Any]:
    """Ghi nhan "Bridge/nguoi van chuyen da thay gi" - **khong mang gi tri chung minh**.

    Dung de phuc vu tra doi doi tac nội bộ. Ben xac minh **không được** dùng
    truong nay de quyet dinh bien nhan co hop le hay khong.
    """
    entry = {
        "role": "transporter",
        "alg": "Ed25519",
        "kid": kid,
        "transporter_id": transporter_id,
        "sig": _b64u(signature),
        "evidentiary_weight": "none",
    }
    attested = dict(receipt)
    attested["transporter_attestations"] = list(
        receipt.get("transporter_attestations", [])) + [entry]
    return attested


class VerificationReport:
    """Ket qua kiem chung bien nhan: trạng thái + tung luu kiem da chay."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.checks: List[str] = []

    def passed(self, label: str) -> None:
        self.checks.append(label)

    def failed(self, label: str, detail: str = "") -> None:
        self.checks.append(label)
        self.errors.append("%s%s" % (label, (": " + detail) if detail else ""))

    @property
    def ok(self) -> bool:
        return not self.errors

    def __bool__(self) -> bool:
        return self.ok

    def summary(self) -> str:
        state = "HOP LE" if self.ok else "KHONG HOP LE"
        return "[%s] %d/%d luu kiem dat - %s" % (
            state,
            len(self.checks) - len(self.errors),
            len(self.checks),
            "; ".join(self.errors) if self.errors else "khong co loi",
        )


def verify_receipt(
    receipt: Mapping[str, Any],
    public_keys: Mapping[str, bytes],
    *,
    now: Optional[str] = None,
    task: Any = None,
    result: Any = None,
    require_unexpired: bool = True,
) -> VerificationReport:
    """Kiem chung bien nhan **khong can tin vao Bridge**.

    ``public_keys``: anh xa ``kid`` -> khoa cong khai Ed25519 (32 byte).
    ``now``: chuoi ISO-8601 de so sanh ``expires_at``; mac dinh la thoi diem
    hien tai (UTC).
    """
    report = VerificationReport()

    if receipt.get("receipt_version") != RECEIPT_VERSION:
        report.failed("phien ban bien nhan", "khong phai %s" % RECEIPT_VERSION)
        return report
    report.passed("phien ban bien nhan")

    for field in ("receipt_id", "trace_id", "issued_at", "expires_at", "nonce",
                  "subject", "parties", "signatures"):
        if not receipt.get(field):
            report.failed("truong bat buoc", "%s thieu hoac rong" % field)
    if report.errors:
        return report
    report.passed("truong bat buoc")

    subject = receipt["subject"]
    for field in ("task_digest", "result_digest"):
        if not subject.get(field):
            report.failed("subject", "%s thieu" % field)
    if report.errors:
        return report
    report.passed("subject")

    if require_unexpired:
        from datetime import datetime, timezone

        try:
            expiry = datetime.fromisoformat(str(receipt["expires_at"]).replace("Z", "+00:00"))
        except ValueError:
            report.failed("han dung", "expires_at khong phai chuoi ISO-8601 hop le")
            return report
        if now is None:
            current = datetime.now(timezone.utc)
        else:
            current = datetime.fromisoformat(str(now).replace("Z", "+00:00"))
        if current >= expiry:
            report.failed("han dung", "bien nhan da het han (%s)" % receipt["expires_at"])
        else:
            report.passed("han dung")

    if task is not None:
        expected = canonical.digest_of(
            canonical.DOMAIN_RECEIPT, canonical.canonical_json(task))
        if expected != subject["task_digest"]:
            report.failed("task digest", "khong khop noi dung task duoc cung cap")
        else:
            report.passed("task digest")
    if result is not None:
        expected = canonical.digest_of(
            canonical.DOMAIN_RECEIPT + "/result", canonical.canonical_json(result))
        if expected != subject["result_digest"]:
            report.failed("result digest", "khong khop noi dung ket qua duoc cung cap")
        else:
            report.passed("result digest")

    payload = signing_payload(receipt)
    executor_sigs = [s for s in receipt["signatures"] if s.get("role") == "executor"]
    if not executor_sigs:
        report.failed("chu ky executor", "khong co chu ky nao tu executor")
        return report

    for signature_entry in executor_sigs:
        kid = signature_entry.get("kid")
        public_key = public_keys.get(kid)
        if public_key is None:
            report.failed("chu ky executor", "khong tim thay khoa cong khai cho kid=%s" % kid)
            continue
        try:
            raw = _unb64u(signature_entry["sig"])
        except Exception:
            report.failed("chu ky executor", "chu ky khong phai base64url hop le")
            continue
        try:
            good = ed25519.verify(public_key, payload, raw)
        except ed25519.VerificationError as exc:
            report.failed("chu ky executor", str(exc))
            continue
        if good:
            report.passed("chu ky executor")
        else:
            report.failed("chu ky executor", "chu ky khong hieu luc")

    if report.ok:
        report.passed("tong hop")
    return report
