# Chính Sách Bảo Mật (Security Policy)

**Phiên bản:** v1.0 · **Hiệu lực:** 21/10/2026 · **Phạm vi:** kho `ai2ai-core` (Apache 2.0)

---

## 1. Phạm vi và trạng thái hiện tại

Kho này chứa **mã PoC minh hoạa**, chạy hoàn toàn bằng thư viện chuẩn Python và **không có tài khoản quản trị**, không có API key, không có dữ liệu người dùng.

| Hạng mục | Trạng thái |
| :--- | :--- |
| Xác thực / phiên làm việc | **Không có** — không phát hành token, không lưu dữ liệu |
| Kết nối ra ngoài (egress) | **Không có** — mã chỉ dùng `hashlib`, `json`, `uuid`, `datetime`, `typing` |
| Tiến trình con (subprocess) | **Không có** |
| Xử lý dữ liệu cá nhân | **Không có** — dữ liệu mô phỏng (synthetic) |
| Phụ thuộc bên thứ ba | **Không có** (`requirements.txt` không tồn tại) |
| Bảo mật chuỗi cung ứng | SHA-256 băm trên từng gói Skill; `scripts/license_gate.py` chạy trong CI |

> **Lưu ý trung thực:** Biên nhận xác thực (Verification Receipt) trong PoC dùng **SHA-256 để chứng minh tính toàn vẹn dữ liệu
> (integrity), chưa chống được chối bỏ danh tính (non-repudiation)** — việc đó cần chữ ký bất đối xứng (Ed25519/DID).
> Xem Issue #2 trong tab Issues.

---

## 2. Báo cáo lỗ hổng

**Chúng tôi hoan nghĩa mọi báo cáo lỗ hổng**, kể cả từ người chưa đóng góp.

| Kênh | Địa chỉ | Ghi chú |
| :--- | :--- | :--- |
| Email | `nan_ai2ai@proton.me` | **Kênh ưu tiên** — kèm tiêu đề `[SECURITY]` |
| Issue | Tab Issues → Security | Dùng khi **không** muốn công khai ngay |

**Không** báo lỗ hổng qua kênh công khai (Issue/PR) nếu lỗi đó chưa được vá.

### Thông tin nên cung cấp

1. Mô tả lỗi và tác động (ảnh hưởng tới tính toàn vẹn, khả dụng, hay quyền riêng tư)
2. Cách tái hiện (script/đầu vào/lệnh)
3. Phiên bản Python và hệ điều hành
4. Bằng chứng (ảnh chụp màn hình, log, traceback)

### Kỳ vọng về thời gian phản hồi

| Giai đoạn | Thời gian mục tiêu |
| :--- | :--- |
| Xác nhận đã nhận | 7 ngày |
| Đánh giá mức độ | 14 ngày |
| Công bố (khi đã vá) | Cùng bản phát hành vá |

> **Cam kết thực tế:** dự án do **một người duy nhất** vận hành với khoảng **10 giờ/tuần**. Các mốc trên là *mục tiêu
> thực tế*, không phải cam kết SLA do tổ chức bảo lãnh. Nếu báo cáo của bạn không được phản hồi, đó là giới hạn
> thật của mô hình này — và chúng tôi ghi nhận điều đó công khai.

---

## 3. Phạm vi không thuộc trách nhiệm

- Thư viện, dịch vụ và chuẩn bên thứ ba được nhắc tới (MCP, A2A, GB/Z 185-2026, DEFA) — lỗi của họ thuộc về họ.
- Mọi kịch bản tấn công vào hệ thống thương mại ngoài phạm vi dự án này.

## 4. Phiên bản trước đây

| Phiên bản | Ngày | Thay đổi |
| :--- | :--- | :--- |
| v1.0 | 21/10/2026 | Ấn phẩm đầu tiên |
