# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Ed25519 thuần Python theo RFC 8032 (Josefsson & Liusvaara, 2017).

Vì sao tự viết?
---------------
Dự án cam kết **Zero Dependencies** (README, mục "Chạy Thử Nghiệm Trong 60 Giây").
Thư viện ``cryptography`` và ``PyNaCl`` đều là gói PyPI, nên cả hai đều phá vỡ cam
kết đã công bố. Python 3.11 cũng **không** có Ed25519 trong ``hashlib``.
Vì vậy bản tham chiếu này dùng **chỉ** ``hashlib`` + số nguyên lớn.

Cảnh báo an toàn (đọc trước khi dùng)
--------------------------------------
1. **KHÔNG constant-time.** Triển khai Python thuần không đảm bảo thời gian
   hằng số. Chỉ dùng để ký/kiểm chứng **dữ liệu công khai** (chữ ký biên nhận
   xác thực). Tuyệt đối KHÔNG dùng để bảo vệ bí mật, khóa API hay mật khẩu.
2. **Chỉ là bản tham chiếu phục vụ giáo dục**, chưa phải mã production.
   Trước khi dùng cho tài liệu pháp lý, hãy đổi sang backend đã kiểm định
   (``cryptography`` / HSM) qua lớp trừu tượng trong ``nan_ai2ai.receipt``.
3. Kiểm chứng bằng **vector chính thức RFC 8032 §7.1** (5 vector, trong
   ``tests/test_ed25519.py``) và đối chiếu chéo với một hiện thực độc lập.

Tham chiếu: https://www.rfc-editor.org/rfc/rfc8032.txt
"""

from __future__ import annotations

import hashlib
from typing import Optional, Tuple

__all__ = [
    "SigningError",
    "VerificationError",
    "generate_keypair",
    "public_from_secret",
    "sign",
    "verify",
]

# --- Tham số đường cong Ed25519 (RFC 8032 §5.1) ---
P = 2 ** 255 - 19
"""Trường số nguyên nguyên tố q = 2^255 - 19."""

L = 2 ** 252 + 27742317777372353535851937790883648493
"""Bậc của điểm đường cong; S trong chữ ký phải nhỏ hơn L."""

D = -121665 * pow(121666, P - 2, P) % P
"""Hằng số d = -121665/121666 (mod p)."""

SQRT_M1 = pow(2, (P - 1) // 4, P)
"""sqrt(-1) mod p, dùng khi giải phương trình bậc hai khi giải mã điểm."""

Point = Tuple[int, int, int, int]
"""Tọa độ mở rộng (X, Y, Z, T) với x = X/Z, y = Y/Z, T = XY/Z."""


class SigningError(Exception):
    """Lỗi khi tạo chữ ký (khoá không hợp lệ, v.v.)."""


class VerificationError(Exception):
    """Lỗi khi kiểm chứng chữ ký (sai định dạng hoặc chữ ký không khớp)."""


def _inv(x: int) -> int:
    """Nghịch đảo modulo p (p là số nguyên tố)."""
    return pow(x, P - 2, P)


def _recover_x(y: int, sign: int) -> int:
    """Giải x từ y và dấu, theo RFC 8032 §5.1.3."""
    if y >= P:
        raise VerificationError("Gia tri y khong hop le")
    x2 = (y * y - 1) * _inv(D * y * y + 1) % P
    if x2 == 0:
        if sign:
            raise VerificationError("Khong ton tai diem xac dinh voi dau nay")
        return 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        raise VerificationError("Khong ton tai diem tren duong cong")
    if (x & 1) != sign:
        x = P - x
    return x


def _point_add(p1: Point, p2: Point) -> Point:
    """Cong hai diem (cong cong to hop "add-2008-hwcd-3", RFC 8032 §5.1.4)."""
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    a = (y1 - x1) * (y2 - x2) % P
    b = (y1 + x1) * (y2 + x2) % P
    c = 2 * t1 * D * t2 % P
    d = 2 * z1 * z2 % P
    e = b - a
    f = d - c
    g = d + c
    h = b + a
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _point_double(p1: Point) -> Point:
    """Nhan doi diem ("dbl-2008-hwcd", RFC 8032 §5.1.4)."""
    x1, y1, z1, _ = p1
    a = x1 * x1 % P
    b = y1 * y1 % P
    c = 2 * z1 * z1 % P
    d = -a % P
    e = ((x1 + y1) * (x1 + y1) - a - b) % P
    g = (d + b) % P
    f = (g - c) % P
    h = (d - b) % P
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def _point_mul(scalar: int, point: Point) -> Point:
    """Nhan diem voi scalar (double-and-add, bit tu MSB xuong LSB)."""
    result: Point = (0, 1, 1, 0)  # diem danh tinh
    while scalar > 0:
        if scalar & 1:
            result = _point_add(result, point)
        point = _point_double(point)
        scalar >>= 1
    return result


def _point_equal(p1: Point, p2: Point) -> bool:
    """So sanh hai diem qua dang ma hoa (tranh truong hop khac toa do nhung cung diem)."""
    x1, y1, z1, _ = p1
    x2, y2, z2, _ = p2
    return (x1 * z2 - x2 * z1) % P == 0 and (y1 * z2 - y2 * z1) % P == 0


def _point_encode(point: Point) -> bytes:
    """Ma hoa diem thanh 32 byte (RFC 8032 §5.1.2)."""
    x, y, z, _ = point
    zinv = _inv(z)
    x = x * zinv % P
    y = y * zinv % P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _point_decode(data: bytes) -> Point:
    """Giai ma 32 byte thanh diem (RFC 8032 §5.1.3)."""
    if len(data) != 32:
        raise VerificationError("Diem ma hoa phai dai dung 32 byte")
    value = int.from_bytes(data, "little")
    sign = value >> 255
    y = value & ((1 << 255) - 1)
    if y >= P:
        raise VerificationError("Gia tri y khong hop le")
    x = _recover_x(y, sign)
    return (x, y, 1, x * y % P)


def _base_point() -> Point:
    """Diem co so B (RFC 8032 §5.1)."""
    y = 4 * _inv(5) % P
    x = _recover_x(y, 0)
    return (x, y, 1, x * y % P)


_BASE = _base_point()


def _secret_scalar(digest: bytes) -> int:
    """Bien khoa bí mat thanh scalar: clamp 3 bit thap, dat bit 254 (RFC 8032 §5.1.5)."""
    a = int.from_bytes(digest[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a


def _secret_expand(secret: bytes) -> Tuple[int, bytes]:
    """Mo rong khoa 32 byte thanh (scalar, prefix 32 byte) theo RFC 8032 §5.1.5."""
    if len(secret) != 32:
        raise SigningError("Khoa bi mat phai dai dung 32 byte")
    digest = hashlib.sha512(secret).digest()
    return _secret_scalar(digest), digest[32:]


def generate_keypair() -> Tuple[bytes, bytes]:
    """Sinh cap khoa (khoa bi mat, khoa cong khai), moi 32 byte.

    Voi PoC, khoa duoc sinh tu ``os.urandom``. Trong san xuat phai dung
    nguon ngau nhien deu kiem chung (CSPRNG) va luu tru ngoai.
    """
    import os

    secret = os.urandom(32)
    return secret, public_from_secret(secret)


def public_from_secret(secret: bytes) -> bytes:
    """Suy ra khoa cong khai 32 byte tu khoa bi mat 32 byte."""
    scalar, _ = _secret_expand(secret)
    return _point_encode(_point_mul(scalar, _BASE))


def sign(secret: bytes, message: bytes) -> bytes:
    """Ky ``message`` bang khoa bi mat Ed25519, tra ve chu ky 64 byte.

    Thuat toan: RFC 8032 §5.1.6.
    """
    if not isinstance(message, (bytes, bytearray)):
        raise SigningError("message phai la bytes")
    message = bytes(message)
    scalar, prefix = _secret_expand(secret)
    public = _point_encode(_point_mul(scalar, _BASE))

    r = int.from_bytes(hashlib.sha512(prefix + message).digest(), "little") % L
    r_point = _point_encode(_point_mul(r, _BASE))

    k = int.from_bytes(hashlib.sha512(r_point + public + message).digest(), "little") % L
    s = (r + k * scalar) % L
    return r_point + int.to_bytes(s, 32, "little")


def verify(public: bytes, message: bytes, signature: bytes) -> bool:
    """Kiem chung chu ky Ed25519. Tra ``True`` khi hieu luc.

    Thuat toan: RFC 8032 §5.1.7. Kiem tra ``S < L`` de chong chu ky "mutable"
    (RFC 8032 §8.4).
    """
    if not isinstance(message, (bytes, bytearray)):
        raise VerificationError("message phai la bytes")
    if len(public) != 32:
        raise VerificationError("Khoa cong khai phai dai dung 32 byte")
    if len(signature) != 64:
        return False

    message = bytes(message)
    r_bytes = signature[:32]
    s = int.from_bytes(signature[32:], "little")
    if s >= L:
        return False

    try:
        point_a = _point_decode(public)
        point_r = _point_decode(r_bytes)
    except VerificationError:
        return False

    k = int.from_bytes(hashlib.sha512(r_bytes + public + message).digest(), "little") % L
    left = _point_mul(s, _BASE)
    right = _point_add(point_r, _point_mul(k, point_a))
    return _point_equal(left, right)
