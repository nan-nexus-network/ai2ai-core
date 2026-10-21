# 05 — Hướng Dẫn Cho Người Đóng Góp Mới (Contributor Onboarding)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026

---

## 1. Bạn cần bao nhiêu thời gian?

| Việc | Thời gian ước tính |
| :--- | :--- |
| Chạy demo lần đầu | **1 phút** |
| Đọc tóm tắt whitepaper (chương 1 + tóm tắt) | **10 phút** |
| Đọc whitepaper đầy đủ (7 chương) | **45 phút** |
| Chạy 6 unit test | **30 giây** |
| Gửi PR đầu tiên | **1–3 giờ** (tùy đầu việc) |

> Dự án **không có** yêu cầu cài đặt gì ngoài Python 3.8+. Không có `pip install`. Không có
> database. Không có API key.

---

## 2. Năm phút đầu tiên

```bash
git clone https://github.com/nan-nexus-network/ai2ai-core.git
cd ai2ai-core
python examples/01-hello-agent/hello_bridge.py     # xem kịch bản 4 bước
python -m unittest discover -s tests -v            # phải ra 6/6 OK
python scripts/license_gate.py                     # phải ra exit 0
```

Cả ba lệnh trên phải chạy được **trên máy sạch**, không cần cài gì thêm.

---

## 3. Bốn đầu việc đã sẵn (chọn cái này nếu chưa biết bắt đầu từ đâu)

| Issue | Nội dung | Kỹ năng cần | Ước lượng |
| :--- | :--- | :--- | :--- |
| **#1** | Thay danh sách từ khóa cấm bằng kiểm tra **cấu trúc** an toàn | Python | 2–4 giờ |
| **#2** | Thêm chữ ký bất đối xứng **Ed25519** cho biên nhận xác thực | Python, crypto | 4–8 giờ |
| **#3** | Viết bộ unit test bổ sung cho luồng dịch MCP → A2A | unittest | 1–2 giờ |

Đầu việc **#3** là nơi tốt nhất để bắt đầu: không cần hiểu kiến trúc chỉ số.

---

## 4. Quy trình gửi PR

1. **Mở Issue trước** nếu đầu việc chưa có Issue (tránh làm trùng). Mô tả: vấn đề, đề xuất, tiêu chí nghiệm thu.
2. **Fork** repo → tạo nhánh từ `main`: `git checkout -b feature/ten-cua-ban`
3. **Làm thay đổi nhỏ.** PR lớn khó review hơn nhiều lần so với 2 PR nhỏ.
4. **Chạy 3 lệnh kiểm tra** (mục 2). Cả 3 phải xanh.
5. **Mở PR** và điền mẫu PR. Tự review diff của mình trước khi gửi.
6. **Chờ review.** PR không có review sẽ **tự động hợp nhất sau 21 ngày** nếu đã đủ review và CI xanh
   (xem [02_GOVERNANCE_PUBLIC](02_GOVERNANCE_PUBLIC.md) mục 3).

### Quy tắc bất di bất dịch

| ✅ Được | ❌ Không |
| :--- | :--- |
| Chỉ dùng thư viện chuẩn Python 3.8+ | Thêm dependency bên thứ ba |
| Có SPDX header ở 5 dòng đầu mỗi file mới | Sửa file không liên quan trong cùng PR |
| Tương thích Python 3.8 | Dùng `match`, `dict \| dict`, `list[str]`, `removeprefix()` |
| Bình luận bằng tiếng Việt hoặc tiếng Anh | Chê bai cá nhân hoặc người đóng góp khác |
| Nêu cách kiểm chứng trong mô tả PR | Đưa dữ liệu cá nhân, khóa hay token vào repo |

---

## 5. Kiểm tra trước khi gửi

```bash
python -m unittest discover -s tests -v     # 6/6 PASS
python examples/01-hello-agent/hello_bridge.py   # exit 0
python scripts/license_gate.py              # exit 0
make test        # tương đương lệnh trên
make license-check
```

CI chạy thêm: quét secret (TruffleHog), test trên Python 3.8 / 3.10 / 3.12, và quét ScanCode.

---

## 6. Lộ trình vai trò

```
  Bậc 1                    Bậc 2                       Bậc 3
Contributor  ──────────►  Module Reviewer  ──────────►  Core Maintainer
≥ 1 PR                  ≥ 3 PR + review ổn định      ≥ 60 ngày đóng góp
                                                                        + đề cử của Bậc 2
```

Chi tiết đầy đủ: [../../CONTRIBUTOR_LADDER.md](../../CONTRIBUTOR_LADDER.md).

---

## 7. Sau khi gửi PR

| Tình huống | Điều gì sẽ xảy ra | Bạn cần làm gì |
| :--- | :--- | :--- |
| CI xanh, có 1 review → hợp nhất | PR được hợp nhất | Không cần làm gì thêm |
| CI xanh, chưa có review | Chờ tối đa 21 ngày | Nhắc nhở sau 1 tuần nếu cần |
| CI đỏ | Báo lỗi chi tiết | Sửa và push lại |
| Bị từ chối | Ghi rõ lý do trong PR | Đọc [02_GOVERNANCE_PUBLIC](02_GOVERNANCE_PUBLIC.md) mục 3 nếu muốn khiếu nại |

---

## 8. Câu hỏi thường gặp

**Tôi không phải lập trình viên chuyên nghiệp — có thể đóng góp không?**
Có. Dự án này được tạo ra bởi một người cũng không phải. Đầu việc #3 (unit test) là nơi tốt nhất để bắt đầu.

**Tôi có thể dùng mã nguồn này cho dự án thương mại không?**
Có. Apache 2.0 cho phép cả mục đích thương mại. Chỉ cần giữ thông báo bản quyền và ghi rõ nếu bạn đã sửa
(xem [../../LICENSE](../../LICENSE)).

**Tôi có thể dùng tên "NAN AI2AI" trong sản phẩm của mình không?**
Không — tên và nhãn hiệu được bảo lưu riêng. Bạn có thể ghi *"Powered by / Forked from NAN AI2AI-SI2SI"*
(xem [../../TRADEMARK.md](../../TRADEMARK.md)).

**Báo lỗ hổng bảo mật thế nào?**
**Không** mở Issue công khai. Xem [../../SECURITY.md](../../SECURITY.md).

**Ai trả lời Issue của tôi?**
Người duy trì, trong vòng 7 ngày nếu có thể. Dự án do một người vận hành ~10 giờ/tuần — xem
[../../SUPPORT.md](../../SUPPORT.md).
