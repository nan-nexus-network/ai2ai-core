# 01 — Kế Hoạch Công Khai (Launch Plan)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026

---

## 1. Nguyên tắc

Ra mắt **một lần, đúng, và có thể đo được** — tốt hơn nhiều lần ra mắt lan man rồi im lặng.
Dự án này có nguồn lực **1 người · ~10 giờ/tuần · 0 đồng**; mỗi lần ra mắt tiêu tốn một khoảng
ngân sách thời gian mà không có dự phòng. Vì vậy kế hoạch này ưu tiên **đúng một lần phát hành công khai**
rồi đo phản hồi thật, thay vì phát hành lặp.

---

## 2. Bốn Cổng (Gates) — nguyên tắc Fail-Closed

Mỗi cổng phải **PASS trước khi** đi tiếp. Cổng nào chưa đạt thì **dừng ở cổng đó** — không "làm tạm",
không "chấp nhận rủi ro để kịp hạn".

| Cổng | Tên | Điều kiện PASS | Trạng thái 21/10/2026 |
| :--- | :--- | :--- | :--- |
| **G1** | **Nội dung & Thương hiệu** | Tài liệu thảo luận & thông điệp có phiên bản nhất quán; tuyên bố minh bạch đủ 5 điểm; thương hiệu đúng bản | ✅ **PASS** — xem thay đổi phiên bản `v0.4-draft` |
| **G2** | **Pháp lý & Giấy phép** | `LICENSE` + `CLA.md` + `TRADEMARK.md` + `HANDOVER.md` đầy đủ; mọi trích dẫn pháp lý đã đối chiếu; cổng license CI xanh | ✅ **PASS** — trích dẫn đã đối chiếu 21/10 (xem `docs/WHITEPAPER…md` mục tham khảo) |
| **G3** | **An toàn & Kỹ thuật** | CI xanh trên 3 phiên bản Python; quét secret không phát hiện; 0 dependency ngoài stdlib; `license_gate.py` exit 0 | ✅ **PASS** — xem [06_RELEASE_CHECKLIST.md](06_RELEASE_CHECKLIST.md) |
| **G4** | **Sẵn sàng phát hành** | Tài khoản/link ngoài đã tạo thật; placeholder đã thay; form ký đã ký; checklist đánh dấu đủ | ⏳ **CHƯA ĐẠT — 6 việc còn lại, xem mục 4** |

> **G4 là cổng quyết định.** G1–G3 đều là điều kiện kỹ thuật. G4 là điều kiện **thực tế**: nếu còn
> một link chết hoặc một placeholder trên trang đích thì dự án **không được** công bố.

---

## 3. Cổng G4 — 6 việc còn lại

Đây là những việc **chỉ người khởi xướng** mới làm được (cần tài khoản thật, không làm tự động được).

| # | Việc | Vì sao chặn | Cách kiểm tra |
| :---: | :--- | :--- | :--- |
| 1 | **Tạo GitHub org + repo** `nan-nexus-network/ai2ai-core` | Mọi link trong README/whitepaper/web_hub trỏ tới đây | Mở `https://github.com/nan-nexus-network/ai2ai-core` → không còn 404 |
| 2 | **Tạo tài khoản Proton Mail** `nan_ai2ai@proton.me` | Là **địa chỉ liên hệ duy nhất** công khai | Gửi thử 1 email, nhận được |
| 3 | **Deploy `web_hub/`** lên Cloudflare Workers → `https://nan-ai2ai.nexusasianetwork.workers.dev` | Là "Cổng thông tin" trong README + whitepaper | DNS phân giải được |
| 4 | **Tạo tài khoản X.com** `@Nan_ai2ai_vn` (`https://x.com/Nan_ai2ai_vn`) | Kênh đối thoại quốc tế | Mở link → tài khoản tồn tại |
| 5 | **Tạo nhóm Zalo/Telegram** (`https://zalo.me/g/h0cbluccgocfud9fmih4` / `https://t.me/+87ARJ1e1NUA0ZDQ1`) | Kết nối cộng đồng builder kỹ thuật | Mở link → vào được nhóm thật |
| 6 | **Ký form phát hành** (checkbox G4) | Xác nhận phạm vi phát hành | Bản ký đã tick 1 trong 2 ô |

> **Không có cổng nào được "bỏ qua" để kịp hạn.** Nếu cần, hãy **lùi ngày phát hành** thay vì phát hành
> với link chết. Một lần ra mắt có 1 link chết tệ hơn nhiều lần ra mắt có 0 link chết.

---

## 4. Sau khi phát hành — 30 ngày đầu

| Tuần | Việc | Đầu ra |
| :--- | :--- | :--- |
| **Tuần 1** | Theo dõi Issue đầu tiên; trả lời trong 48 giờ nếu có thể | Báo cáo tuần đầu |
| **Tuần 2** | Rà soát mọi Issue → phân loại thành *lỗi thật* / *đóng góp được* / *thảo luận* | Nhãn đúng trên mọi Issue |
| **Tuần 3** | Chốt 2–3 đầu việc đầu tiên trong tab Issues (dánh nhãn `good first issue`) | Việc đủ cụ thể để người khác nhảy vào |
| **Tuần 4** | Báo cáo tháng đầu tiên (theo [03_METRICS](03_METRICS_AND_MEASUREMENT.md)) | Báo cáo công khai |

### Nguyên tắc 30 ngày đầu

- **Trả lời mọi Issue**, kể cả khi câu trả lời là "chưa làm được, và đây là lý do".
- **Không đóng Issue chỉ vì im lặng.** Nếu không xử lý được, ghi rõ lý do và đóng với nhãn `wontfix — đã ghi nhận`.
- **Không hứa thời gian** cho việc chưa có người nhận.

---

## 5. Điều KHÔNG làm trong giai đoạn công khai

| ❌ Không | Vì sao |
| :--- | :--- |
| Phát hành "v0.2", "v0.3" liên tiếp | Không có nguồn lực để duy trì; mỗi bản phát hành là một cam kết bảo trì |
| Thêm dependency bên thứ ba | Phá vỡ cam kết Zero Dependencies và thêm bề mặt tấn công |
| **Không** nhận tiền, **không** gọi vốn, **không** phát hành token | Vi phạm cam kết bất biến |
| Tuyên bố "đã sẵn sàng cho production" | PoC chưa qua hậu kiểm độc lập |
| Tuyên bố đại diện cho cộng đồng AI Việt Nam | Vi phạm tuyên bố minh bạch |

---

## 6. Điều kiện dừng (Kill Criteria)

Dự án **dừng phát hành công khai** và quay về trạng thái riêng nếu xảy ra bất kỳ điều sau:

1. Không thể tạo hoặc duy trì đủ 3 tài khoản ngoài (GitHub, Proton, Cloudflare Pages).
2. `license_gate.py` hoặc CI **fail** trên `main`.
3. Phát hiện rò rỉ dữ liệu cá nhân hoặc khóa bí mật.
4. Người khởi xướng không thể duy trì **cam kết 10 giờ/tuần** trong **4 tuần liên tiếp**.

> Điều kiện 4 là điều kiện **thật** và chúng tôi ghi công khai. Một kho mở bị bỏ rơi vì không ai duy trì
> tệ hơn một kho mở không bao giờ mở. [HANDOVER.md](../../HANDOVER.md) đã cam kết trao quyền tiếp quản
> cho cộng đồng nếu điều này xảy ra — hãy dùng cơ chế đó thay vì để kho im lặng.
