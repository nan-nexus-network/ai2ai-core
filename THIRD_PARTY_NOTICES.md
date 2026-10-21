# THÔNG BÁO VỀ THÀNH PHẦN BÊN THỨ BA (THIRD-PARTY NOTICES)

Dự án **NAN AI2AI-SI2SI** được cấp phép theo các điều khoản của [Apache License 2.0](LICENSE).

Tài liệu này cung cấp thông báo về bản quyền, giấy phép và các thành phần phần mềm của bên thứ ba được sử dụng hoặc tham chiếu trong kho lưu trữ này, nhằm tuân thủ Điều 4(d) của Giấy phép Apache 2.0.

---

## 1. Môi trường Thực thi & Thư viện Hiện tại (PoC v0.1)

Mã nguồn mẫu hiện tại trong thư mục `examples/01-hello-agent/hello_bridge.py` và bộ kiểm thử `tests/test_hello_bridge.py` được thiết kế theo nguyên tắc **Zero External Dependencies** (Không phụ thuộc thư viện ngoài):

* **Python Standard Library:** Toàn bộ quá trình thực thi chỉ sử dụng các thư viện chuẩn đi kèm ngôn ngữ Python 3.8+ (bao gồm `json`, `uuid`, `hashlib`, `sys`, `datetime`, `typing`, `unittest`, `importlib.util`).
  * Giấy phép: **Python Software Foundation (PSF) License Agreement**.
  * Bản quyền: © Python Software Foundation.
  * Thư viện chuẩn Python không yêu cầu tuyên bố ghi nhận bản quyền đặc thù trong phân phối mã nguồn.

* **Thư viện ngoài bổ sung:**
  * Hiện tại: **Không có** (0 thư viện ngoài / No third-party runtime dependencies).
  * Dự án chạy độc lập không yêu cầu thực hiện `pip install` bất kỳ gói phần mềm nào.

---

## 2. Giao diện Web Hub (`web_hub/index.html`)

* Toàn bộ mã nguồn HTML và CSS của trang Cổng thông tin (Landing Hub) được viết thuần (Vanilla HTML/CSS).
* Hệ thống sử dụng System Font Stack gốc của hệ điều hành người dùng (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `sans-serif`), không tải phông chữ từ máy chủ bên thứ ba.
* Không sử dụng bất kỳ framework giao diện hay thư viện JavaScript của bên thứ ba nào.

---

## 3. Quy định Cập nhật Trong Tương lai

Tệp này sẽ được Ban Quản trị dự án cập nhật định kỳ khi phát sinh các thành phần phụ thuộc mới:

* Khi tích hợp các thư viện mật mã học chuyên dụng (ví dụ: `cryptography` cho khóa bất đối xứng Ed25519) hoặc bộ kiểm tra JSON Schema (`jsonschema`), tên gói phần mềm, liên kết mã nguồn gốc, bản quyền tác giả và văn bản giấy phép tương ứng sẽ được công bố chi tiết tại đây.
* Mọi đóng góp từ cộng đồng có mang theo mã nguồn bên thứ ba phải tuân thủ các giấy phép nguồn mở tương thích với Apache License 2.0 (như MIT, BSD, ISC, Apache 2.0) và không được vi phạm bản quyền hoặc bằng sáng chế độc quyền.
