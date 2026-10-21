# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""NAN AI2AI-SI2SI: Open Reference Framework (chưa phải Protocol).

Gói mã nguồn tham chiếu mở. Xem ``docs/ADR_001.md`` (định vị) và
``docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`` (mô hình biên nhận có chữ ký).

Tất cả mô đun trong gói này chỉ dùng **thư viện chuẩn Python** (stdlib),
để giữ đúng cam kết "Zero Dependencies" đã công bố trong README.
"""

__version__ = "0.2.0-dev"

__all__ = [
    "canonical",
    "ed25519",
    "receipt",
    "trust",
    "validation",
]
