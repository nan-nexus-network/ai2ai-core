## Loại thay đổi

- [ ] Sửa lỗi (bug fix)
- [ ] Tính năng mới
- [ ] Tài liệu
- [ ] Bảo trì (dependency, CI, refactor) — **không** đổi hành vi

## Vấn đề đang giải quyết

<!-- Số issue: Closes #NNN. Nếu chưa có issue, mô tả ngắn vấn đề. -->

## Cách thay đổi

<!-- Mô tả ngắn gọn. Nếu thêm/xoá code, giải thích vì sao cách này đúng. -->

## Kiểm chứng

<!-- Quan trọng: cho biết bạn đã chạy gì và kết quả ra sao. -->

- [ ] `python -m unittest discover -s tests -v` — 10/10 PASS
- [ ] `python examples/01-hello-agent/hello_bridge.py` — exit 0
- [ ] `python scripts/license_gate.py` — exit 0
- [ ] Tài liệu cập nhật (nếu thay đổi hành vi công khai)

## Checklist

- [ ] Không thêm dependency ngoài thư viện chuẩn Python
- [ ] Code mới có SPDX header `Apache-2.0` ở 5 dòng đầu
- [ ] Không đưa vào dữ liệu cá nhân, khóa, token hay thông tin nội bộ
- [ ] Tương thích Python 3.8+
- [ ] Đã tự review diff của mình

<!-- Bạn đồng ý với CLA.md khi mở PR. -->
