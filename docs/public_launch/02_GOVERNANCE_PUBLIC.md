# 02 — Quản Trị Công Khai (Public Governance)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026

> Bản rút gọn của [../../GOVERNANCE.md](../../GOVERNANCE.md), dành cho người đọc không tham gia phát triển.
> Nếu có mâu thuẫn giữa hai tài liệu, [../../GOVERNANCE.md](../../GOVERNANCE.md) là bản quyết định.

---

## 1. Ba nguyên tắc không thay đổi

1. **Mọi quyết định có người chịu trách nhiệm bằng tên.**
2. **Người viết code không tự phê duyệt phần việc của mình.**
3. **Không rút lại.** Mọi phiên bản đã phát hành dưới Apache 2.0 là tài sản chung vĩnh viễn.

---

## 2. Ai làm gì

| Bạn muốn... | Ai quyết | Bạn cần |
| :--- | :--- | :--- |
| Góp ý về lập luận trong Tài liệu Thảo Luận | Người đóng góp + Maintainer | Mở Issue |
| Gửi PR sửa code / tài liệu | Maintainer review | PR + checklist trong mẫu PR |
| Nhận đầu việc nhỏ | Maintainer gán nhãn | Nhận `good first issue` |
| Được nâng lên Bậc 2 (Reviewer) | Maintainer, theo [CONTRIBUTOR_LADDER](../../CONTRIBUTOR_LADDER.md) | ≥ 3 PR đã hợp nhất |
| Báo lỗ hổng bảo mật | Người báo + Maintainer | [SECURITY.md](../../SECURITY.md) — **không** mở Issue công khai |
| Phát hành phiên bản mới | **Founder** | Đề xuất từ Maintainer |
| Nhận quyền quản trị kho | Founder, theo cam kết 12 tháng | [HANDOVER.md](../../HANDOVER.md) |

---

## 3. Bất đồng ý kiến — bốn bậc, không bao giờ bế tắc

Mỗi bậc có **thời hạn cụ thể**. Hết thời hạn thì chuyển bậc kế tiếp. Bậc cuối **ghi nhận** bất đồng
thay vì cố giải quyết — và bất đồng được lưu lại, không bị xoá.

```
   Bậc 1            Bậc 2              Bậc 3              Bậc 4
 Thảo luận   →   Đề xuất rõ ràng →  Quyết định     →   Ghi nhận
   7 ngày            7 ngày          Maintainer          bất đồng
                                     7 ngày          (đóng issue)
```

| Bậc | Cơ chế | Thời hạn | Nếu hết hạn |
| :--- | :--- | :--- | :--- |
| 1 | Thảo luận tự do trên Issue/PR | 7 ngày | → Bậc 2 |
| 2 | Người mở viết **đề xuất cụ thể** (mục tiêu, phạm vi, tiêu chí nghiệm thu). Người phản hồi trả lời **đồng ý** hoặc **không đồng ý + lý do**. | 7 ngày | → Bậc 3 |
| 3 | Maintainer quyết định theo tiêu chí kỹ thuật đã ghi, ghi vào PR | 7 ngày | → Bậc 4 |
| 4 | Ghi rõ **điểm bất đồng còn lại** và **lý do không thực hiện được**, đóng issue với nhãn `wontfix — đã ghi nhận bất đồng` | — | **Đóng. Không mở lại.** |

### Vì sao không có deadlock

- Bậc 3 là **điểm dừng bắt buộc** — có quyền quyết cuối trong phạm vi kỹ thuật.
- Bậc 4 **lưu giữ** bất đồng thay vì giải quyết.
- Người đóng góp luôn có quyền **rút PR** và mở issue mới — không mất gì.
- **Không có tình huống nào dẫn tới việc một bên im lặng vĩnh viễn mà không có dấu vết.**

### Nếu không có phản hồi

Không phản hồi sau **21 ngày** kể từ lần liên hệ cuối → PR được gắn nhãn `needs-review` và **tự động hợp nhất
khi đã đủ review và vượt qua toàn bộ CI**. Một đóng góp đúng không nên bị chôn vì người duy trì bận.

---

## 4. Minh bạch quyết định

Quyết định ở Bậc 3 và Bậc 4 được ghi trong PR hoặc issue tương ứng. Chúng tôi **không xoá bất đồng** —
chúng tôi **ghi nhận** nó. Một kho mở mà không ai biết ai quyết định gì không phải kho mở, đó là hộp đen.

---

## 5. Xung đột lợi ích

Người khởi xướng vừa là tác giả vừa là Acceptance Authority. Đây là xung đột lợi ích **đã biết**. Giảm thiểu:

- Quyết định kỹ thuật thuần tuý do Maintainer đưa ra, Founder **không** can thiệp.
- Mọi phát hành đều kèm kiểm chứng CI công khai mà bất kỳ ai đều chạy lại được.
- Lịch sử commit là bản ghi bất biến — không thể viết lại lịch sử.

---

## 6. Thay đổi quy trình này

Đề xuất thay đổi quy trình → mở Issue với nhãn `governance`. Thay đổi có hiệu lực khi được Maintainer chấp thuận
**và** được phản ánh trong commit tương ứng.
