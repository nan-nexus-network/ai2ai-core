# Issue #1: [Security / PoC] Thay thế bộ lọc từ khóa tĩnh (Blocklist) bằng cơ chế kiểm tra cấu trúc an toàn hơn

**Nhãn (Labels):** `good first issue`, `help wanted`, `security`

## Mô tả vấn đề (Problem Description)
Hiện tại hàm `sanitize_and_validate` trong `examples/01-hello-agent/hello_bridge.py` đang dùng danh sách từ khóa cấm ("drop table", "system override", "ignore previous instructions") quét trên toàn bộ chuỗi JSON.

Cách này dễ gây lỗi chặn nhầm (**false-positive**) đối với dữ liệu hợp lệ (ví dụ: ghi chú hàng hóa hợp pháp `"drop table shipment at port"` sẽ bị chặn nhầm vì chứa cụm từ `"drop table"`).

## Mục tiêu (Expected Behavior)
Đề xuất hoặc gửi Pull Request (PR) tách riêng:
1. Kiểm tra cấu trúc kiểu dữ liệu từng trường (strict field-level validation).
2. Tách lớp kiểm tra Prompt Injection theo ngữ nghĩa (Semantic Classifier / Allowlist Schema) thay vì quét chuỗi tĩnh thô.
3. Chỉ sử dụng thư viện chuẩn của Python (`json`, `re`, `typing`).
