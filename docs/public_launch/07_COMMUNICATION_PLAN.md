# 07 — Kế Hoạch Truyền Thông 90 Ngày (Public Communication Plan)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026 · **Phạm vi:** công khai, không phát hành

> **Nguyên tắc của kế hoạch này:** ta **không** đăng bài để tạo cảm giác thành công. Ta đăng bài để
> **tìm ra người có thể phản biện**. Một bài viết không ai phản biện là một bài viết không ai đọc.

---

## 1. Nguyên tắc bất biến của thông điệp

| # | Luôn nói | Không bao giờ nói |
| :---: | :--- | :--- |
| 1 | Đây là **PoC**, chưa phải giao thức hoàn chỉnh | "Sẵn sàng cho production" |
| 2 | **12 câu hỏi mở**, chờ trả lời | "Chúng tôi đã giải quyết vấn đề" |
| 3 | Không xin tiền, không gọi vốn, không phát hành token | Bất kỳ ám chỉ nào về tài trợ/lợi nhuận |
| 4 | Không đại diện cho cộng đồng AI Việt Nam | "Thay mặt cộng đồng" |
| 5 | Mọi thứ dùng **100% công cụ mở, 0 đồng** | Số liệu tài chính/dự phóng không có nguồn |
| 6 | Người khởi xướng **không phải** lập trình viên chuyên nghiệp | Che giấu điều này |
| 7 | Nêu rõ **giới hạn kỹ thuật** | Giấu giới hạn |

> **Về con số:** chỉ công bố những gì **đo được và tái lập được**. Nếu không có lệnh kiểm tra trong repo
> thì đó là ước tính — và phải ghi là ước tính. Xem [03_METRICS](03_METRICS_AND_MEASUREMENT.md) mục 4.

---

## 2. Kênh — chỉ dùng kênh đã có thật

| Kênh | Vai trò | Ưu tiên | Điều kiện dùng |
| :--- | :--- | :--- | :--- |
| **Kho GitHub** | Nơi chính của đối tượng kỹ thuật | **P0** | Repo đã public |
| **Tài liệu thảo luận (Markdown)** | Tài liệu gốc, luôn cập nhật | **P0** | Luôn |
| **Website / Landing Page** | Cổng thông tin | **P0** | Đã deploy |
| **LinkedIn** | Tiếp cận doanh nghiệp & chuyên gia | P1 | Đã có tài khoản |
| **Nhóm Zalo / Telegram** | Thảo luận cộng đồng | P1 | Đã có nhóm thật |
| **YouTube** | Giải thích trực quan | P2 | Có năng lực làm video |
| **Báo chí / hiệp hội** | Đối tác thể chế | P2 | Có câu chuyện đã kiểm chứng |
| **WeChat / kênh Trung Quốc** | Thị trường mục tiêu | P2 | Chỉ khi có năng lực duy trì |

> **Quy tắc:** **không mở kênh mới nếu chưa duy trì được kênh hiện tại.** Một kênh bỏ hoang 3 tháng
> còn tệ hơn không có kênh nào.

---

## 3. Lịch 90 ngày

### Tháng 1 — Cài đặt nền tảng

| Tuần | Việc | Kênh | Đầu ra |
| :--- | :--- | :--- | :--- |
| 1 | Mở repo + Issue template + `good first issue` | GitHub | Repo sẵn sàng nhận PR |
| 2 | Đăng **bài giới thiệu #1** (vấn đề + 12 câu hỏi mở) | Website, LinkedIn | 1 bài |
| 3 | Đăng **bài giới thiệu #2** (kỹ thuật: bridge làm gì, khác proxy ra sao) | Website, LinkedIn | 1 bài |
| 4 | **Báo cáo tuần 1–4** + đăng bài giới thiệu #3 | Issue `meta` | 1 bài + 1 báo cáo |

### Tháng 2 — Tìm người phản biện

| Tuần | Việc | Đầu ra |
| :--- | :--- | :--- |
| 5 | Bài #4: **"Tại sao không dùng A2A của Google luôn?"** — câu hỏi khó nhất, trả lời thẳng | 1 bài |
| 6 | Bài #5: "4 giới hạn kỹ thuật mà chúng tôi **không** giải quyết được" | 1 bài |
| 7 | Bài #6: "Chúng tôi đã sai ở đâu" — tổng hợp phản biện đã nhận | 1 bài |
| 8 | **Báo cáo tháng 1** + đăng bài #7 | 1 báo cáo + 1 bài |

### Tháng 3 — Mở rộng và đo

| Tuần | Việc | Đầu ra |
| :--- | :--- | :--- |
| 9 | Bài #8: "Kết quả 90 ngày, kể cả những gì **không** đạt" | 1 bài |
| 10 | Hợp nhất PR cộng đồng đầu tiên + kể lại quá trình | 1 PR + 1 bài |
| 11 | Bài #9: "Bài toán mở tiếp theo — và tại sao chúng tôi **chưa** giải" | 1 bài |
| 12 | **Báo cáo tháng 3 + tổng kết 90 ngày** + cập nhật `ROADMAP.md` | 1 báo cáo |

**Tổng:** 9 bài · 3 báo cáo tuần đầu + 3 báo cáo tháng + 1 tổng kết.

### Định tần suất

- **LinkedIn:** 3 bài/tuần (mục tiêu) — nhưng **chỉ khi đã có kênh thật**.
- **Website:** cập nhật theo bài đăng.
- **Báo cáo:** tuần (Thứ Sáu) + tháng (ngày 28).

---

## 4. Cấu trúc một bài đăng (dùng chung)

1. **Một câu hỏi thật** ở đầu — câu mà người đọc thực sự quan tâm.
2. **Điều chúng tôi đang thử** (2–3 đoạn).
3. **Những gì chúng tôi CHƯA làm được** — luôn có, không phải phụ lục.
4. **Một câu hỏi cụ thể cho người đọc** — câu hỏi có thể trả lời trong Issue.
5. **Link** tới tài liệu gốc + link tạo Issue.

> **Quy tắc tuyệt đối:** mỗi bài phải có **mốc 3 và mốc 4**. Bài nào thiếu giới hạn hoặc thiếu câu hỏi
> thì **không đăng**.

---

## 5. Ấn phẩm dự kiến

| # | Ấn phẩm | Kênh chính | Loại |
| :---: | :--- | :--- | :--- |
| 1 | "Việt Nam có nên xây tầng giao thức AI?" | LinkedIn, Website | Giới thiệu |
| 2 | "Cầu nối giao thức khác proxy server ra sao?" | LinkedIn, Website | Kỹ thuật |
| 3 | "Chúng tôi đã dựng được gì trong 60 giây" | Website, X | Demo |
| 4 | "Tại sao không dùng A2A của Google?" | LinkedIn, Website | Phản biện |
| 5 | "4 giới hạn chúng tôi không giải quyết được" | LinkedIn, Website | Minh bạch |
| 6 | "Những chỗ chúng tôi đã sai" | Website | Minh bạch |
| 7 | "Kết quả 30 ngày đầu" | LinkedIn | Báo cáo |
| 8 | "90 ngày: kết quả thật" | LinkedIn, Website | Báo cáo |
| 9 | "Bài toán mở tiếp theo" | LinkedIn | Mời tham gia |

> **Không** phát hành bài trước khi repo public. Trước đó, mọi bài chỉ dẫn tới repo **riêng tư** — nếu
> chưa có repo public thì **chưa đăng bài nào**.

---

## 6. Xử lý phản hồi tiêu cực

Tuân theo [04_RISK_REGISTER](04_RISK_REGISTER_AND_CONTINGENCY.md) mục 3. Tóm tắt:

| Tình huống | Phản ứng |
| :--- | :--- |
| Chỉ trích **đúng** | Cảm ơn công khai, sửa, ghi vào `CHANGELOG.md` |
| Chỉ trích **đúng nhưng ngoài phạm vi** | Ghi rõ phạm vi hiện tại, không hứa |
| Chỉ trích **sai** | Chỉ ra bằng dẫn chứng cụ thể từ tài liệu, không đáp bằng cảm tính |
| Công kích cá nhân | Xử lý theo [CODE_OF_CONDUCT](../../CODE_OF_CONDUCT.md), công khai |
| Chỉ trích lặp lại điểm đã sửa | Lỗi của chúng tôi — sửa và ghi nhận |

---

## 7. Rủi ro của kế hoạch truyền thông

| Rủi ro | Dấu hiệu sớm | Ứng phó |
| :--- | :--- | :--- |
| **Quá nhiều bài, không đủ chất lượng** | ≥ 3 bài chưa có phản hồi nào | Dừng lịch, hỏi lại 12 câu hỏi mở |
| **Bài bị hiểu sai là "AI Việt làm chuẩn"** | Bình luận kiểu "Việt Nam đi đầu AI" | Tuyên bố minh bạch **đặt ở đầu bài**, không đặt ở cuối |
| **Bài bị trích nhầm là tuyên bố chính thức** | Bài báo dùng mà không nêu nguồn | Nêu rõ "thảo luận độc lập, không đại diện" ở mọi ấn phẩm |
| **Tài khoản bị spam/bot** | Comment lạ | Bật moderation GitHub; không xoá bình luận thật |
| **Báo đưa tin sai** | Bài sai tiêu đề | Phản hồi bằng link trực tiếp tới đoạn cần kiểm chứng; **không** phản công bằng giọng điệu |

---

## 8. Điều kiện để bắt đầu lịch

| # | Điều kiện | ✅ |
| :---: | :--- | :�� |
| 1 | Repo GitHub **đã public** và truy cập được không cần đăng nhập | ☐ |
| 2 | Website đã deploy | ☐ |
| 3 | **Đầu việc #1, #2, #3 đã đăng** trong tab Issues | ☐ |
| 4 | Hộp thư liên hệ **đã nhận được** email | ☐ |
| 5 | `CHANGELOG.md` đã ghi "Chưa phát hành" | ☐ |
| 6 | Đã đọc [05_CONTRIBUTOR_ONBOARDING](05_CONTRIBUTOR_ONBOARDING.md) và biết sẽ trả lời Issue thế nào | ☐ |

> **Nếu chưa đủ 10/10 — chưa đăng bài nào.** Đăng bài rồi mà không có nơi nhận phản hồi thì chỉ tạo ấn tượng xấu.
