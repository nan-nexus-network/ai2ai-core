---
name: ISSUE 1 SECURITY BLOCKLIST
about: Security / PoC: Thay thế bộ lọc từ khóa cấm (Blocklist) bằng cơ chế kiểm tra cấu trúc an toàn hơn
labels: [good first issue, help wanted, security]
assignees: []
---

**Nhãn (Labels):** `good first issue`, `help wanted`, `security`

## Trạng thái

🟢 **ĐÃ XỬ LÝ Ở v0.2** — xem `nan_ai2ai/validation.py` và `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md` (Quyết định 1).

Bộ kiểm tra mới dùng **allowlist schema**: kiểm tra kiểu dữ liệu, độ dài, miền giá trị, và **từ chối mọi trường không nằm trong schema**. Blocklist tĩnh được giữ lại như lớp phòng thủ thứ hai, không phải lớp chính.

## Mô tả vấn đề gốc (đã đóng một phần)
Hiện tại hàm `sanitize_and_validate` trong `examples/01-hello-agent/hello_bridge.py` đang dùng danh sách từ khóa cấm ("drop table", "system override", "ignore previous instructions") quét trên toàn bộ chuỗi JSON.

Cách này dễ gây lỗi chặn nhầm (**false-positive**) đối với dữ liệu hợp lệ (ví dụ: ghi chú hàng hóa hợp pháp `"drop table shipment at port"` sẽ bị chặn nhầm vì chứa cụm từ `"drop table"`).

## Mục tiêu (Expected Behavior)
Đề xuất hoặc gửi Pull Request (PR) tách riêng:
1. Kiểm tra cấu trúc kiểu dữ liệu từng trường (strict field-level validation).
2. Tách lớp kiểm tra Prompt Injection theo ngữ nghĩa (Semantic Classifier / Allowlist Schema) thay vì quét chuỗi tĩnh thô.
3. Chỉ sử dụng thư viện chuẩn của Python (`json`, `re`, `typing`).

> **Lưu ý về phạm vi:** bộ kiểm tra mới là **subset** của JSON Schema Draft 2020-12, không phải bản triển khai đầy đủ. Từ khoá ngoài subset (`$ref`, `if/then/else`, `unevaluatedProperties`, `contains`, `dependentSchemas`, `format`…) **gây lỗi tường minh** thay vì bị bỏ qua âm thầm. Mở rộng subset là một đầu việc riêng — xem `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`.
