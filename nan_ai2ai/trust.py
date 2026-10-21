# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Mô hình neo tin cậy cho biên nhận có chữ ký.

Quyet dinh thiet ke (xem ``docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md``)
---------------------------------------------------------------------------
Ba phuong an duoc can nhac:

  A. **Registry tap trung** - mot noi luu khoa cong khai cua moi agent.
     -> **BAO LOI**: ROADMAP ghi ro "khong cung cap dich vu, API hay ha tang chay
        that"; du an mot nguoi, khong co nguon luc van hanh. Trai ADR-001.
  B. **DID** (did:web / DID-WBA nhu ANP dung) - dinh danh phan tan co chu ky.
     -> **De lai**: cong thuc thuc thi co, nhung lai bat buoc phai co ha tang
        resolver va vong doi tin cay (DID document, WebVH). Vuot xa nang luc
        hien tai, va khong can de **chung minh** mot bien nhan.
  C. **TOFU (trust-on-first-use) + Agent Card** - ben xac minh **ghim** khoa
     cong khai lan dau tien nhin thay; sau do moi lan xac minh phai dung
     dung khoa da ghim.
     -> **CHON**: khong can ha tang, khong can chay dich vu, dung ngay.

Quyet dinh: **C**, nhung **khong khoa cua vai tro**:
  - ``kid`` = JWK thumbprint (RFC 7638) - dinh danh khoa, khong can registry.
  - Agent Card la **ke phan phoi** khoa cong khai. The huong A2A: card co
    truong ``signatures`` (JWS) + ``security_requirements`` theo tung skill
    (xem ``specification/a2a.proto`` cua ``a2aproject/A2A``).
  - Du an **khong** phat minh lai Agent Card. ``agent_card`` o day tao ra
    mot card ** toi gian, **tuong thich ve hinh dang** voi A2A Agent Card.
  - DID **khong bi loai tranh**: neu mot agent co DID, DID co the nam trong
    truong ``did`` cua card. Form cua bien nhan khong phu thuoc DID.

**Hanh han bi thuong nhat cua TOFU** (phai noi ro, khong giu im):
  - TOFU bao ve duoc **ke tu lan tiep xuc thu hai**, khong bao ve duoc **lan
    tiep xuc dau tien**. Mot ke phong mitm o thoi diem bam dau co the thay
    khoa truoc khi ben xac minh ghim.
  - Voi muc do tin cay cao, can them mot trong: khoa cong khai ngoai tuyen
    (out-of-band), hoac **transparency log** (append-only) de chung minh khoa
    da duoc cong bo public. Ca hai deu de dua vao roadmap v0.3+, khong phai
    thuoc pham vi v0.2.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional

from . import receipt as receipt_mod

__all__ = [
    "TrustConflictError",
    "TrustStore",
    "agent_card",
    "verify_with_store",
]


class TrustConflictError(Exception):
    """Khoa cong khai da ghim khac voi khoa moi nhin thay - can canh bao thu cong."""


class TrustStore:
    """Kho ghim khoa cong khai theo mo hinh TOFU.

    Luu ``kid`` -> khoa cong khai. Lan dau tien: ghim. Lan sau:
      - cung khoa -> OK
      - khac khoa -> ``TrustConflictError`` (dau hieu tuong tam khoa)
    """

    def __init__(self) -> None:
        self._pins: Dict[str, bytes] = {}

    def __len__(self) -> int:
        return len(self._pins)

    def __contains__(self, kid: str) -> bool:
        return kid in self._pins

    def pins(self) -> Dict[str, bytes]:
        """Tra ve ban sao cua cac ghim hien co."""
        return dict(self._pins)

    def get(self, kid: str) -> Optional[bytes]:
        return self._pins.get(kid)

    def pin(self, kid: str, public_key: bytes) -> bool:
        """Ghim khoa. Tra ``True`` neu la lan ghim dau tien.

        Nem ``TrustConflictError`` neu ``kid`` da duoc ghim voi khoa khac.
        """
        if len(public_key) != 32:
            raise ValueError("Khoa cong khai Ed25519 phai dai 32 byte")
        existing = self._pins.get(kid)
        if existing is None:
            self._pins[kid] = bytes(public_key)
            return True
        if existing != public_key:
            raise TrustConflictError(
                "kid %s da duoc ghim voi mot khoa khac. "
                "Dieu nay co the la tuong tai khoa, hoac bi tuong tam. "
                "KHONG nen tu dong ghim lai - can nguoi xac nhan." % kid)
        return False

    def check(self, kid: str, public_key: bytes) -> bool:
        """Kiem tra khoa co khop voi ghim hien co hay khong."""
        existing = self._pins.get(kid)
        return existing is not None and existing == bytes(public_key)


def agent_card(
    *,
    agent_id: str,
    public_key: bytes,
    capabilities: Optional[list] = None,
    endpoint: str = "",
    did: str = "",
    skills: Optional[list] = None,
    card_signature: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Tao mot Agent Card ** toi gian, tuong thich ve hinh dang voi A2A**.

    Day KHONG phai Agent Card chinh thuc cua A2A. Day la mot bieu muc **nho**,
    lay truc tu Agent Card cua A2A nhung chi giu nhung truong NAN thuc su can:

    ==================  ==========================================================
    ``name``            ten dinh danh cua agent
    ``description``     mo ta ngan
    ``version``         phien ban cua bo mo ta
    ``provider``        to chuc phu trách
    ``capabilities``    nang luc
    ``skills``          danh sach ky nang
    ``supportedInterfaces``  giao dien (endpoint) ho tro
    ``signatures``      chu ky JWS cua chinh card (co the rong trong PoC)
    ``securityRequirements``  yeu cau bao mat theo ky nang
    ==================  ==========================================================

    Khoa cong khai Ed25519 duoc mang trong ``x5c``-tuong-duong: truong
    ``publicKeyJwk`` (JWK dang base64url) + ``kid`` (thumbprint RFC 7638).

    Ve A2A: ``specification/a2a.proto`` khai bao ``AgentCard.signatures``
    la "JSON Web Signatures computed for this AgentCard" va
    ``security_requirements`` theo tung skill. Ban nay dung **cung ten truong**
    de co the gan truc tiep, nhung **khong** phai ban trien khai A2A.
    """
    jwk = {
        "crv": "Ed25519",
        "kty": "OKP",
        "x": _b64u(public_key),
    }
    card: Dict[str, Any] = {
        "name": agent_id,
        "description": "Agent Card toi gian cua NAN AI2AI (tuong thich hinh dang A2A, khong phai ban A2A chinh thuc)",
        "version": "0.2.0-dev",
        "provider": {"organization": "NAN AI2AI", "url": "https://github.com/nan-nexus-network/ai2ai-core"},
        "capabilities": dict(capabilities or {"streaming": False, "pushNotifications": False}),
        "skills": list(skills or []),
        "supportedInterfaces": [
            {"url": endpoint, "protocolBinding": "nan-receipt/v1"} if endpoint else
            {"url": "", "protocolBinding": "nan-receipt/v1"}
        ],
        "publicKeyJwk": jwk,
        "kid": receipt_mod.jwk_thumbprint(public_key),
        "securityRequirements": [],
        "signatures": [card_signature] if card_signature else [],
    }
    if did:
        card["did"] = did
    return card


def _b64u(data: bytes) -> str:
    import base64

    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def card_to_json(card: Mapping[str, Any]) -> str:
    """Chuoi JSON dung de luu/phe tanh Agent Card (can dinh dang, khoa sap xep)."""
    return json.dumps(card, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def verify_with_store(
    receipt: Mapping[str, Any],
    store: TrustStore,
    *,
    now: Optional[str] = None,
    task: Any = None,
    result: Any = None,
):
    """Kiem chung bien nhan **va** khoa phai dung khoa da ghim.

    Day la duong dan xac minh "khong can tin Bridge": ben xac minh chi can
    mot kho da ghim (TOFU) + chu ky cua executor.
    """
    public_keys: Dict[str, bytes] = {}
    for entry in receipt.get("signatures", []):
        if entry.get("role") != "executor":
            continue
        kid = entry.get("kid")
        pinned = store.get(kid) if kid else None
        if pinned is not None:
            public_keys[kid] = pinned
    return receipt_mod.verify_receipt(
        receipt, public_keys, now=now, task=task, result=result)
