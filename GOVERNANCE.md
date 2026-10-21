# Quản Trị Dự Án (Project Governance)

**Phiên bản:** v1.0 · **Hiệu lực:** 21/10/2026 · **Phạm vi công khai:** kho `ai2ai-core`

> Tài liệu này mô tả **cách dự án ra quyết định khi có người ngoài tham gia**. Bộ quy tắc ứng xử cộng đồng nằm ở
> [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md); lộ trình vai trò nằm ở [CONTRIBUTOR_LADDER.md](CONTRIBUTOR_LADDER.md).

---

## 1. Nguyên tắc

1. **Mọi quyết định đều có người chịu trách nhiệm bằng tên.**
2. **Vai trò Executor và vai trò Verifier tách biệt.** Người viết code không tự phê duyệt phần việc của mình.
3. **Không có thay đổi trạng thái phát hành nào diễn ra trong im lặng.** Mọi phê duyệt phải để lại dấu vết.
4. **Fail-Closed.** Khi không chắc chắn → dừng lại và ghi nhận, không đoán.
5. **Không rút lại.** Mọi phiên bản đã phát hành dưới Apache 2.0 là tài sản chung vĩnh viễn ([HANDOVER.md](HANDOVER.md)).

---

## 2. Ai quyết định gì

| Quyết định | Quyền quyết định | Cần tham mưu |
| :--- | :--- | :--- |
| Nội dung kỹ thuật, thuật toán, định dạng giao thức | **Người đóng góp** (qua PR) sau khi có ít nhất 1 review của Maintainer | Maintainer |
| Thêm / sửa bài viết trong Tài liệu Thảo Luận | Maintainer | Người đóng góp |
| Sửa lỗi bảo mật | **Người báo cáo** + Maintainer cùng xác nhận | — |
| Đóng góp `CLA.md`, nâng bậc vai trò | Maintainer | — |
| **Phát hành phiên bản mới** | **Người khởi xướng (Founder)** — là Acceptance Authority duy nhất | Maintainer + hội đồng kỹ thuật |
| **Trao quyền tiếp quản kho lưu trữ** | Founder, theo cam kết 12 tháng trong [HANDOVER.md](HANDOVER.md) | — |
| Thay đổi giấy phép | **Không ai** — Apache 2.0 là vĩnh viễn | — |

### Nguyên tắc tách vai trò

> Người viết code **không** tự phê duyệt phần việc của mình. Một PR cần **ít nhất một review từ người khác**
> trước khi được hợp nhất. Đây là điều kiện bắt buộc của CI (`ci.yml`), không phải thói quen.

---

## 3. Xử lý bất đồng ý kiến — Quy trình leo thang (không deadlock)

Dự án là **một người vận hành**, nên quy trình này được thiết kế để **không bao giờ bế tắc**. Mỗi bậc có
**thời hạn cụ thể**; hết thời hạn thì chuyển bậc kế tiếp (không dừng).

| Bậc | Cơ chế | Thời hạn | Kết quả khi hết hạn |
| :--- | :--- | :--- | :--- |
| **1 — Thảo luận** | Issue hoặc PR comment. Người mở và người phản hồi cùng nêu lập luận. | 7 ngày | Sang bậc 2 |
| **2 — Đề xuất rõ ràng** | Người mở viết **đề xuất cụ thể** (mục tiêu, phạm vi, rủi ro, tiêu chí nghiệm thu). Người phản hồi trả lời **đồng ý** hoặc **không đồng ý + lý do**. | 7 ngày | Sang bậc 3 |
| **3 — Quyết định của Maintainer** | Maintainer quyết định theo tiêu chí kỹ thuật đã ghi. Quyết định được ghi vào PR. | 7 ngày | Sang bậc 4 |
| **4 — Ghi nhận bất đồng** | Nếu vẫn bất đồng: Maintainer ghi rõ **điểm bất đồng còn lại** và **lý do không thể thực hiện**, đóng issue với nhãn `wontfix — đã ghi nhận bất đồng`. | — | **Đóng. Không mở lại.** |

### Vì sao không có deadlock

- Bậc 3 có **quyền quyết cuối cùng** trong phạm vi kỹ thuật — đó là điểm dừng bắt buộc.
- Bậc 4 **ghi lại bất đồng thay vì giải quyết** — bất đồng được lưu giữ, không bị xoá.
- Người đóng góp luôn có quyền **rút lại PR** và mở lại issue mới — không mất gì.
- Người khởi xướng **không** can thiệp vào bất đồng kỹ thuật thuần tuý giữa cộng đồng.

### Nếu Maintainer không phản hồi

Nếu không có phản hồi sau **21 ngày** kể từ lần liên hệ cuối: PR được gắn nhãn `needs-review` và
**tự động hợp nhất khi đủ review** nếu đã vượt qua toàn bộ kiểm tra CI. Việc này đảm bảo một đóng góp
đúng vẫn không bị chôn vì người duy trì bận.

---

## 4. Chính sách nhánh

- `main` — nhánh phát hành, luôn phải qua CI.
- PR từ fork: **CI chạy với `pull_request`** → không cần quyền ghi.
- Không dùng `git push --force` lên `main`.

## 5. Minh bạch quyết định

Mọi quyết định ở bậc 3 và 4 đều được ghi trong PR hoặc issue tương ứng. Chúng tôi **không** xoá bất đồng —
chúng tôi **ghi nhận** nó. Đây là lý do tài liệu này tồn tại: một kho mở mà không ai biết ai quyết định gì
thì không phải kho mở, đó là một hộp đen.

## 6. Liên hệ

Câu hỏi về quản trị → mở Issue với nhãn `governance` hoặc email `nan_ai2ai@proton.me`.
