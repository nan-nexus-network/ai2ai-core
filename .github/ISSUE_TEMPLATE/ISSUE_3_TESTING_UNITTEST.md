---
name: ISSUE 3 TESTING UNITTEST
about: Testing: Viết bộ Unit Test bổ sung cho luồng dịch MCP sang A2A
labels: [good first issue, testing]
assignees: []
---

**Nhãn (Labels):** `good first issue`, `testing`

## Mô tả vấn đề (Problem Description)
Để người mới tải kho lưu trữ về có thể kiểm tra tự động trên GitHub Actions (CI/CD), dự án cần một bộ kiểm thử tự động cơ bản.

## Mục tiêu (Expected Behavior)
1. Tạo tệp `tests/test_hello_bridge.py` sử dụng thư viện chuẩn `unittest` của Python.
2. Kiểm thử 3 kịch bản:
   - Kịch bản 1: Gói tin hợp lệ → Trả về `True` và sinh `bridged_packet` chuẩn A2A.
   - Kịch bản 2: Gói tin thiếu trường bắt buộc → Trả về `False` kèm thông báo lỗi trường cụ thể.
   - Kịch bản 3: Gói tin chứa chuỗi Prompt Injection đáng ngờ → Bị chặn bởi `sanitize_and_validate`.
