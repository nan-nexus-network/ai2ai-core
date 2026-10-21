# Issue #2: [Cryptography] Bổ sung cơ chế chữ ký số (Ed25519 / HMAC) bên cạnh mã băm SHA-256 trong Verification Receipt

**Nhãn (Labels):** `good first issue`, `enhancement`, `cryptography`

## Mô tả vấn đề (Problem Description)
Biên nhận kiểm chứng `issue_verification_receipt` trong `examples/01-hello-agent/hello_bridge.py` hiện mới dùng `hashlib.sha256` để chứng minh tính toàn vẹn (Integrity) của gói tin tại thời điểm chuyển dịch qua Bridge.

Tuy nhiên, SHA-256 thuần túy **chưa chống được giả mạo danh tính người gửi (Non-repudiation)** vì không có khóa bí mật (Secret Key) hoặc hạ tầng định danh phân tán (DID).

## Mục tiêu (Expected Behavior)
1. Thảo luận hoặc viết một ví dụ nhỏ (`02-signed-receipt`) minh họa cách hai Agent ký số xác nhận gói tin (sử dụng HMAC hoặc Ed25519).
2. Giữ mã nguồn gọn nhẹ, hạn chế tối đa dependencies ngoài.
