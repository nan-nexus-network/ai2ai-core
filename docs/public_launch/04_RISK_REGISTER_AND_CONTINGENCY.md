# 04 — Sổ Rủi Ro & Kịch Bản Ứng Phó (Risk Register & Contingency)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026 · **Rà soát:** hằng quý

> Sổ này được viết để **có sẵn phương án ứng phó** trước khi sự việc xảy ra — không phải để viết sau.
> Vì dự án do một người vận hành, mỗi kịch bản dưới đây đều bắt đầu bằng câu hỏi
> *"nếu chuyện này xảy ra vào lúc 2 giờ sáng thì tôi làm gì?"*

---

## 1. Rủi ro kỹ thuật

| ID | Rủi ro | Khả năng | Tác động | Phương án ứng phó | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | Người duy trì không phản hồi Issue/PR | **Cao** | Trung bình | Tự động hợp nhất sau 21 ngày nếu đủ review + CI xanh (xem [02_GOVERNANCE_PUBLIC](02_GOVERNANCE_PUBLIC.md) mục 3) | ✅ Đã cài |
| T-02 | Reviewer duy nhất nghỉ việc / rời dự án | Trung bình | Cao | Tách vai trò Executor/Verifier; mỗi PR cần ≥ 2 review khi có ≥ 2 maintainer | 🟡 Cần bổ sung quy tắc |
| T-03 | Người đóng góp gửi PR chứa ý định xấu (dependency độc hại, code tối ưu cho AI) | Trung bình | Cao | Review bắt buộc; CI cấm import ngoài stdlib; `license_gate.py` chặn package copyleft | ✅ Đã cài |
| T-04 | Người khởi xướng rời đi / burnout | **Cao** | **Rất cao** | Cam kết 12 tháng bàn giao trong [HANDOVER.md](../../HANDOVER.md); giữ vai trò Maintainer có thể tiếp quản | 🟡 Xem mục 2 |
| T-05 | Lỗ hổng bảo mật được công bố trước khi vá | Trung bình | Cao | [SECURITY.md](../../SECURITY.md) — kênh báo cáo riêng, cấm mở Issue công khai | ✅ Đã cài |

---

## 2. Kịch bản mất người (Key-Person Risk) — chi tiết

Đây là rủi ro **lớn nhất** của dự án, vì mọi quyết định hiện đi qua một người.

### 2.1. Người khởi xướng không còn duy trì được

| Mốc | Việc | Kết quả |
| :--- | :--- | :--- |
| **Tuần 1–2** | Dừng nhận việc mới; ghi rõ trạng thái trong Issue `meta` | Cộng đồng biết dự án đang tạm dừng, **không** tưởng đã chết |
| **Tuần 2–4** | Bàn giao vai trò Maintainer cho ít nhất 1 người đạt Bậc 2 | Có người review được |
| **Tuần 4–8** | Chuyển quyền phát hành cho người đó | Dự án không phụ thuộc một cá nhân |
| **Sau 12 tháng** | Kích hoạt cam kết bàn giao trong [HANDOVER.md](../../HANDOVER.md) | Quyền quản trị kho trao cho cộng đồng |

### 2.2. Điều **không** làm

- ❌ Không im lặng biến mất. Im lặng là tín hiệu tệ hơn một thông báo rõ ràng.
- ❌ Không "tạm dừng" rồi quay lại mà không nói với ai. Kỳ vọng của cộng đồng phải được nói rõ.
- ❌ Không giữ bí mật về việc mình đang không có thời gian. Sự trung thực về năng lực là giá trị của dự án này.

### 2.3. Thứ đã có sẵn

- [HANDOVER.md](../../HANDOVER.md) — cam kết bàn giao 12 tháng, viết từ trước khi cần.
- [CONTRIBUTOR_LADDER.md](../../CONTRIBUTOR_LADDER.md) — Bậc 2 đã có quyền triage, Bậc 3 có quyền hợp nhất.
- [02_GOVERNANCE_PUBLIC.md](02_GOVERNANCE_PUBLIC.md) mục 3 — cơ chế tự động hợp nhất khi Maintainer im lặng.

---

## 3. Kịch bản bị chỉ trích công khai

| Bước | Hành động |
| :--- | :--- |
| **1. Trong 24 giờ** | **Đọc toàn bộ.** Trả lời lời chỉ trích ngay trên kênh nó xuất hiện. Không xoá, không ẩn, không khóa tài khoản. |
| **2. Trong 24 giờ** | Phân loại: (a) đúng và cần sửa → ghi nhận + sửa; (b) đúng nhưng ngoài phạm vi hiện tại → ghi rõ phạm vi; (c) sai → **chỉ ra bằng dẫn chứng cụ thể**, không đáp lại bằng cảm tính. |
| **3. Trong 48 giờ** | Nếu chỉ trích chạm điểm cốt lõi (giới hạn kỹ thuật, pháp lý, giấy phép) → **cập nhật tài liệu nguồn**, không chỉ trả lời trên mạng. Tài liệu là bản ghi chính. |
| **4. Trong 1 tuần** | Tổng hợp điểm bị chỉ trích đúng vào `CHANGELOG.md` và `ROADMAP.md`. |

### Nguyên tắc

> **Chúng tôi đã công khai 12 câu hỏi mở và 4 rủi ro lớn nhất.** Ai chỉ trích được điểm chúng tôi đã nói
> thì không phải chỉ trích — đó là kiểm chứng. Chúng tôi sẽ cảm ơn và sửa.
>
> Những gì chúng tôi **không** làm: đáp lại bằng giọng điệu công kích, xoá bình luận, đe dọa, hoặc
> gán nhãn cho người chỉ trích.

### Chuỗi bài học

Nếu cùng một điểm bị chỉ trích **lần thứ hai**, đó là lỗi của chúng tôi, không phải của người chỉ trích.
Xem [03_METRICS](03_METRICS_AND_MEASUREMENT.md) mục 4 — chỗ nào chưa đo được thì nói ra.

---

## 4. Kịch bản "thành công vừa phải" — vài người quan tâm, không ai đóng góp

**Đây là kịch bản phổ biến nhất và ít được chuẩn bị nhất.** Nó không phải thất bại, nên không ai báo cáo
nó — nhưng nó cũng không phải thành công, nên không ai vui.

| Dấu hiệu | Chẩn đoán | Hành động |
| :--- | :--- | :--- |
| 3–10 Issue đã đóng, **0 PR** | Người ta đọc nhưng không thấy đường vào | Rút gọn đầu việc đầu tiên xuống còn **một PR một giờ**; đăng 3 `good first issue` cụ thể |
| Issue hỏi "làm thế nào?" nhưng không ai làm | Thiếu hướng dẫn, không thiếu hứng thú | Bổ sung hướng dẫn đóng góp mẫu; trả lời kèm link tới tệp cần sửa |
| Người đọc xem whitepaper nhưng không hỏi gì | Tài liệu chưa **kết thúc bằng một câu hỏi cụ thể** | Mỗi chương kết bằng 1 câu hỏi cụ thể có thể trả lời trong Issue |
| 0 Issue trong 2 tháng | Hoặc không ai đọc, hoặc đọc ở nơi khác | Đo reach bằng kênh có sẵn; nếu không đo được → **công bố là không đo được** |

> **Nguyên tắc:** thành công vừa phải **không phải là thất bại** — nhưng nó cũng không để dự án tự tồn tại.
> Công báo trung thực với chỉ số vừa phải tốt hơn im lặng.

---

## 5. Kịch bản không có người dùng

| Bước | Hành động |
| :--- | :--- |
| **Nhận ra** | Sau 60 ngày: 0 người dùng thử. Ghi nhận trong báo cáo tháng. |
| **Phân biệt nguyên nhân** | (a) Chưa ai biết dự án tồn tại → vấn đề truyền thông; (b) Biết nhưng thấy "đây chỉ là PoC, chưa dùng được" → vấn đề **giá trị**, không phải vấn đề truyền thông. |
| **Nếu là (b)** | **Đừng** đẩy thêm tính năng. Thay vào đó: hỏi trong Issue *"Bạn cần gì từ một cầu nối để dùng được?"* và **ghi lại câu trả lời**. Một PoC không có người dùng là một PoC chưa tìm ra bài toán. |
| **Công bố** | Nếu sau 90 ngày vẫn 0 → công khai điều đó trong báo cáo và trong `ROADMAP.md`. Một PoC thất bại được ghi nhận trung thực có giá trị hơn một PoC bị giấu. |

---

## 6. Kịch bản pháp lý và giấy phép

| Kịch bản | Phản ứng |
| :--- | :--- |
| Người dùng kêu vì giấy phép | Kiểm tra giấy phép gốc của phần việc; nếu từ bản thứ ba → **không** chịu trách nhiệm, chỉ định nguồn; nếu vi phạm → công bố + sửa |
| Người dùng kêu vì khai thác dữ liệu | Repo **không** có API, không lưu dữ liệu → hướng dẫn tới dữ liệu mà họ tự tạo ra |
| Có bên thứ ba đòi giấy phép thương mại | Trả lời theo `LICENSE` + `TRADEMARK.md`; **không** thương lượng giấy phép khác |
| Bị cơ quan chức năng hỏi | Không đại diện, không nhận tài trợ, không cung cấp dịch vụ thương mại → nêu rõ phạm vi PoC; **không** đưa ra cam kết suy diễn |
| Phát hiện giấy phép sai trong hồ sơ của mình | Sửa ngay + công bố trong `CHANGELOG.md`. Không giấu. |

---

## 7. Kịch bản cộng đồng

| Kịch bản | Phản ứng |
| :--- | :--- |
| Tranh luận gay gắt về kỹ thuật | Đây là **điều tốt**. Trả lời ở mức kỹ thuật, nêu bằng chứng, ghi vào Issue |
| Xung đột giữa hai người đóng góp | Áp dụng [02_GOVERNANCE_PUBLIC](02_GOVERNANCE_PUBLIC.md) mục 3 — leo thang 4 bậc, cuối cùng **ghi nhận** |
| Đóng góp có ý đồ xấu | [CODE_OF_CONDUCT](../../CODE_OF_CONDUCT.md) — công khai, xử lý công khai, không im lặng |
| Người đóng góp rời đi sau khi đóng góp lớn | Cảm ơn công khai; giữ nguyên đóng góp; **không** gỡ nhãn hay ghi vào hồ sơ kiểm định |
| Ai đó fork và làm tốt hơn | **Chúc mừng.** Đó là mục tiêu của giấy phép Apache 2.0. Ghi vào `ROADMAP.md` nếu muốn theo dõi |
| Ai đó fork và phá hoại | Không liên quan đến kho gốc. Không công kích lại. Nếu có vi phạm pháp lý → xử lý theo quy trình pháp lý, không theo quy trình cộng đồng |
| Báo đưa tin sai về dự án | Phản hồi bằng **dẫn chứng từ chính tài liệu**, không phản công bằng giọng điệu. Cung cấp liên kết trực tiếp tới đoạn cần kiểm chứng |

---

## 8. Cơ chế rà soát

| Việc | Chu kỳ | Người |
| :--- | :--- | :--- |
| Rà soát sổ này | Hằng quý | Founder |
| Kiểm tra mục nào đã chuyển từ "chưa chuẩn bị" sang "đã có" | Hằng quý | Founder |
| Ghi nhận sự cố đã xảy ra | Ngay khi xảy ra | Founder, trong Issue `meta` |

> **Một sổ rủi ro không bao giờ được cập nhật là một sổ rủi ro không tồn tại.** Sổ này chỉ có giá trị
> nếu nó thay đổi theo thực tế.
