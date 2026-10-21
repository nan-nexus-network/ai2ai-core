---
name: ISSUE 2 CRYPTOGRAPHY ED25519
about: Cryptography: Bổ sung chữ ký số bất đối xứng (Ed25519 / HMAC) cho bản nhận xác thực SHA-256 trong Verification Receipt
labels: [good first issue, enhancement, cryptography]
assignees: []
---

**Nhãn (Labels):** `good first issue`, `enhancement`, `cryptography`

## Trạng thái

🟢 **ĐÃ XỬ LÝ Ở v0.2** — xem `nan_ai2ai/ed25519.py`, `nan_ai2ai/receipt.py`, ví dụ `examples/03-signed-receipt/signed_receipt_demo.py` và `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md` (Quyết định 2).

**Đã làm:**
- Ed25519 thuần Python theo RFC 8032 (giữ cam kết "Zero Dependencies"), kiểm chứng bằng **5 vector chính thức RFC 8032 §7.1** và đối chiếu chéo với `cryptography` (25/25 mẫu ngẫu nhiên khớp tuyệt đối cả khoá công khai lẫn chữ ký).
- Biên nhận `nan-receipt/v1`: **chỉ bên thực thi ký**, có `nonce` + `expires_at` (chống replay), `kid` = JWK thumbprint RFC 7638, băm có domain separator + length prefix.
- Mô hình neo tin cậy: **TOFU** (Quyết định 3 của ADR-002).

**Còn mở:** backend `cryptography`/HSM thay cho bản thuần Python; transparency log để tuyên bố "kiểm chứng độc lập".

## Mô tả vấn đề gốc (đã đóng)
Biên nhận kiểm chứng `issue_verification_receipt` trong `examples/01-hello-agent/hello_bridge.py` hiện mới dùng `hashlib.sha256` để chứng minh tính toàn vẹn (Integrity) của gói tin tại thời điểm chuyển dịch qua Bridge.

Tuy nhiên, SHA-256 thuần túy **chưa chống được giả mạo danh tính người gửi (Non-repudiation)** vì không có khóa bí mật (Secret Key) hoặc hạ tầng định danh phân tán (DID).

## Mục tiêu (Expected Behavior)
1. Thảo luận hoặc viết một ví dụ nhỏ (`02-signed-receipt`) minh họa cách hai Agent ký số xác nhận gói tin (sử dụng HMAC hoặc Ed25519).
2. Giữ mã nguồn gọn nhẹ, hạn chế tối đa dependencies ngoài.
