---
name: ISSUE 3 TESTING UNITTEST
about: Testing: Viết bộ Unit Test bổ sung cho luồng dịch MCP sang A2A
labels: [good first issue, testing]
assignees: []
---

**Nhãn (Labels):** `good first issue`, `testing`

## Trạng thái

🟡 **MỘT PHẦN** — bộ test đã lớn từ **10 lên 100 test** (`python -m unittest discover -s tests -v`): `tests/test_ed25519.py` (17), `tests/test_validation.py` (32), `tests/test_canonical.py` (11), `tests/test_receipt.py` (40).

**Còn mở:** test cho `agent_chat.py` — demo P2P hiện **không** gọi lớp kiểm tra (xem `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`, Hệ quả 6); và test cho biến thể schema khác.

## Mô tả vấn đề gốc (đã đóng một phần)
Để người mới tải kho lưu trữ về có thể kiểm tra tự động trên GitHub Actions (CI/CD), dự án cần một bộ kiểm thử tự động cơ bản.

## Mục tiêu (Expected Behavior)
1. Tạo tệp `tests/test_hello_bridge.py` sử dụng thư viện chuẩn `unittest` của Python.
2. Kiểm thử 3 kịch bản:
   - Kịch bản 1: Gói tin hợp lệ → Trả về `True` và sinh `bridged_packet` chuẩn A2A.
   - Kịch bản 2: Gói tin thiếu trường bắt buộc → Trả về `False` kèm thông báo lỗi trường cụ thể.
   - Kịch bản 3: Gói tin chứa chuỗi Prompt Injection đáng ngờ → Bị chặn bởi `sanitize_and_validate`.
