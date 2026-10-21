# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Chuan hoa du lieu va tinh bam co phan tach mien (domain separation).

Viet sao
--------
``hello_bridge.py`` (v0.1) tinh bam bang cach **noi truc tiep** hai chuoi JSON::

    json.dumps(bridged_packet, sort_keys=True) + json.dumps(execution_output, sort_keys=True)

Cach nay co hai khuyet diem:
  1. **Khong co dau phan cach** -> ranh gioi giua hai blob khong ro rang.
  2. **Khong co version/domain separator** -> cung mot byte payload se cho cung
     mot bam o moi phien ban, khong the phan biet.

``danh_dich`` bo sung:
  - ``canonical_json`` : dau phan cach ``,``/``:`` va sap xep khoa -> byte bi dinh
    nghia duy nhat cho mot doi tuong JSON.
  - ``digest_input``   : them **domain separator** va **do dai dai truoc** moi
    thanh phan, theo nguyen tac "length-prefixed framing" - loai bo hoan toan
    mo hinh "chuoi cong chuoi" (xem RFC 8032 §5.1.5 cho cach nguon dai tuyet doi).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

__all__ = [
    "DOMAIN_RECEIPT",
    "DOMAIN_SIGNATURE",
    "canonical_json",
    "digest_input",
    "sha256_hex",
]


DOMAIN_RECEIPT = "nan-receipt/v1/digest"
"""Mien tach rieng cho bam noi dung bien nhan."""

DOMAIN_SIGNATURE = "nan-receipt/v1/sign"
"""Mien tach rieng cho payload duoc ky. KHONG duoc dung chung voi domain digest."""


def canonical_json(value: Any) -> bytes:
    """Chuan hoa mot doi tuong JSON thanh byte duy nhat.

    Quy tac: ``json.dumps`` voi ``sort_keys=True``, ``separators=(",", ":")``,
    ``ensure_ascii=False``, ma hoa UTF-8.

    ``ensure_ascii=False`` giu nguyen ky tu Unicode thay vì escape ``\\uXXXX``
    -> byte bi dang ky phu thuoc vao bien dich, va giup so sanh giua hai
    trien khai khac nhau (JavaScript, Go) ra cung mot ket qua.
    """
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest_input(domain: str, *parts: bytes) -> bytes:
    """Ghep cac thanh phan thanh mot chuoi byte co **domain separator** va **do dai**.

    Cung thuc::

        digest_input(d, p1, p2) = d.encode() + b"\\x00"
                                 + len(p1).to_bytes(4, "big") + p1
                                 + len(p2).to_bytes(4, "big") + p2

    Do dai 4 byte big-endian cho phep boi qua moi bien dich giong nhau. Bat bu
    phai theo RFC 6962 (Certificate Transparency) va RFC 8032 §5.1.5.
    """
    if not isinstance(domain, str) or not domain:
        raise ValueError("domain phai la chuoi khong rong")
    out = bytearray(domain.encode("ascii"))
    out.append(0)
    for part in parts:
        if not isinstance(part, (bytes, bytearray)):
            raise TypeError("moi thanh phan phai la bytes")
        out += len(part).to_bytes(4, "big")
        out += part
    return bytes(out)


def sha256_hex(data: bytes) -> str:
    """SHA-256 hex (nhan dinh chung, dung cho digest noi dung)."""
    return hashlib.sha256(data).hexdigest()


def digest_of(domain: str, *parts: bytes) -> str:
    """Tien ich: bam SHA-256 hex cua ``digest_input(domain, *parts)``."""
    return sha256_hex(digest_input(domain, *parts))
