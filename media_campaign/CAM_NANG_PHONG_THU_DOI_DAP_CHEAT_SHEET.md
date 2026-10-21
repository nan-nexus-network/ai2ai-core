# CẨM NANG PHÒNG THỦ & ĐỐI ĐÁP TRỰC CHIẾN (CHEAT SHEET)
## BỘ QUY TẮC PHẢN BIỆN, TRẢ LỜI PHỎNG VẤN & XỬ LÝ BÌNH LUẬN CỘNG ĐỒNG

**Mã tài liệu:** `NAN-AI2AI-CHEAT-SHEET-DEFENSE-20261021`  
**Dự án:** NAN AI2AI-SI2SI Core Sandbox  
**Mục đích:** Thuộc lòng phản xạ trong 30 giây khi tiếp xúc kỹ sư, báo chí và cộng đồng mạng.

---

## I. BẢNG 3 CÂU TRẢ LỜI KỸ THUẬT CỐT LÕI (Thuộc Lòng Trong 30 Giây)

| Câu hỏi xoáy từ Kỹ sư | Bản chất cần nhớ | Câu trả lời 3 ý chuẩn xác (Nói trực tiếp hoặc bình luận) |
| :--- | :--- | :--- |
| **1. "Bridge này khác gì một cái Proxy Server hay API Gateway đổi JSON bình thường?"** | Proxy chuyển tiếp đường truyền (byte); Bridge dịch ngữ nghĩa tác vụ và xuất biên nhận kiểm chứng chung. | **1.** Nếu nhìn ở vị trí đứng giữa nhận và chuyển gói tin thì đúng là nó giống một API Gateway.<br/>**2.** Nhưng điểm khác là Proxy chỉ chuyển tiếp đường truyền, còn Bridge can thiệp vào ngữ nghĩa tác vụ: nó dịch từ cấu trúc gọi công cụ (kiểu MCP) sang cấu trúc giao việc (kiểu A2A), kiểm tra hợp đồng dữ liệu (Schema Contract) và xuất biên nhận xác thực chung (SHA-256 Receipt).<br/>**3.** Ở bản PoC 60 giây hiện tại thì logic này đang viết tối giản nhất để minh họa ý tưởng, rất cần anh em góp ý thêm ở phần đàm phán trạng thái. |
| **2. "A2A của Google đã open-source rồi, sao không dùng luôn mà đẻ thêm Bridge làm gì?"** | A2A tốt khi cả 2 bên cùng dùng A2A. Khi 1 bên dùng chuẩn khác thì cần bộ chuyển đổi (adapter) trung lập. | **1.** Đúng là A2A của Google đã mở mã nguồn và rất mạnh nếu cả hai Agent đều viết theo chuẩn A2A.<br/>**2.** Khoảng trống chỉ xuất hiện khi một Agent dùng chuẩn khác (như MCP hoặc chuẩn nội địa của Trung Quốc/EU) cần giao việc cho Agent chuẩn A2A mà không bên nào muốn viết lại hệ thống của mình.<br/>**3.** Thử nghiệm này không tạo ra chuẩn mới để cạnh tranh với A2A, mà chỉ thử làm một mô-đun chuyển đổi trung lập đứng giữa nối các chuẩn đó lại. |
| **3. "Mã băm SHA-256 trong Receipt chứng minh được gì? Bên gửi tự chế ra chuỗi hash đó thì sao?"** | SHA-256 chỉ chứng minh toàn vẹn dữ liệu (không bị sửa), chưa chống được giả mạo danh tính (cần chữ ký số Ed25519). | **1.** Bác bắt đúng điểm yếu nhất của bản PoC rồi: SHA-256 đơn thuần chỉ chứng minh được tính toàn vẹn (Integrity) — tức là đề bài và kết quả khớp nhau tại thời điểm qua Bridge.<br/>**2.** Nó hoàn toàn chưa chống được chối bỏ danh tính (Non-repudiation) vì chưa có khóa bí mật.<br/>**3.** Ở bản tiếp theo bắt buộc phải kết hợp chữ ký số bất đối xứng (như Ed25519/DID) của cả 2 Agent; mình đã mở sẵn Issue #2 trên GitHub về đúng điểm này để nhờ anh em viết giúp. |

---

## II. BỘ 5 CÂU TRẢ LỜI PHỎNG VẤN BÁO CHÍ (Media Response Kit)

### 1. Khi nhà báo hỏi: *"Anh/chị là ai? Vì sao lại ẩn danh?"*
> **Trả lời:** "Tôi làm việc trong mảng nghiên cứu và kết nối dự án. Tôi chọn ẩn danh để tài liệu được đánh giá hoàn toàn bằng chất lượng của 12 câu hỏi mở, không bị chi phối bởi lý lịch cá nhân, đồng thời chứng minh tôi không dùng dự án cộng đồng này để đánh bóng tên tuổi hay gọi vốn. Tôi sẵn sàng trả lời chi tiết mọi câu hỏi chuyên môn qua email."

### 2. Khi nhà báo hỏi: *"Dự án có ai tài trợ hay đứng sau không?"*
> **Trả lời:** "Hoàn toàn không. Ngân sách thực hiện là 0 đồng (Zero Cash), sử dụng 100% công cụ miễn phí (GitHub, Cloudflare Pages) và dưới 10 giờ/tuần của cá nhân tôi. Dự án cam kết không xin tiền, không gọi vốn."

### 3. Khi nhà báo hỏi: *"Không biết lập trình và dùng AI viết thì liệu có đáng tin cậy?"*
> **Trả lời:** "Đó là lý do tôi công khai điều này ngay trang 1 và gọi đây là 'Tài liệu thảo luận mở v0.3-draft'. AI giúp tôi đi 20% quãng đường đầu là hệ thống hóa câu hỏi và dựng code mẫu minh họa, còn 80% tiếp theo cần giới chuyên môn và các kỹ sư thực thụ vào phản biện, kiểm chứng."

### 4. Khi nhà báo hỏi: *"Tại sao là Việt Nam mà không phải Singapore hay Malaysia?"*
> **Trả lời:** "Việt Nam không mạnh nhất về vốn tài chính như Singapore hay trung tâm dữ liệu phần cứng như Malaysia, nhưng lại có vị thế trung lập hiếm có về giao thức kỹ thuật, làm việc sâu với cả hệ sinh thái Mỹ, Âu lẫn Nhật, Hàn, Trung Quốc. Đây là lợi thế hẹp nhưng thực chất để đóng góp các bộ chuyển đổi mã nguồn mở."

### 5. Khi nhà báo hỏi: *"Anh/chị mong muốn đạt được điều gì sau bài báo này?"*
> **Trả lời:** "Tôi chỉ mong 12 câu hỏi mở trong tài liệu — đặc biệt là việc Việt Nam nên chỉ làm người dùng ứng dụng hay nên tham gia nghiên cứu tầng giao thức kết nối — được các chuyên gia và nhà làm chính sách cùng thảo luận. Dù kết luận cuối cùng là giả thuyết của tôi sai và tìm ra hướng khác tốt hơn, tài liệu cũng đã hoàn thành sứ mệnh."

---

## III. KỊCH BẢN ỨNG PHÓ 3 TÌNH HUỐNG BÌNH LUẬN (Tinh Tế / Facebook / Mạng Xã Hội)

### Tình huống A — Bình luận chê bai gay gắt:
*Ý kiến công kích:* "Không biết code, dùng AI đẻ ra mấy chục dòng if-else đổi JSON rồi đòi làm giao thức quốc gia, đúng là ảo tưởng!"

**Cách đối đáp (Điềm tĩnh, cầu thị 100%):**
> "Cảm ơn bác đã nói thẳng. Đúng như bác nhận xét, file hello_bridge.py hiện tại thực chất chỉ là vài chục dòng chuyển đổi JSON và kiểm tra chuỗi cơ bản để minh họa khái niệm trong 60 giây, hoàn toàn chưa đủ tầm gọi là một giao thức hoàn chỉnh. Mình ghi rõ hạn chế này ngay ở mục 3 trong bài và trang đầu tài liệu để tránh gây hiểu lầm. Theo góc nhìn của bác, nếu hai Agent khác chuẩn (ví dụ MCP và A2A) cần xác thực tác vụ với nhau thì bài toán khó nhất ở tầng kỹ thuật là gì? Rất mong bác chỉ giáo thêm."

---

### Tình huống B — Bình luận hỏi sâu kỹ thuật:
*Ý kiến chất vấn:* "Nếu làm Bridge trung lập thì xử lý độ trễ (latency) và trạng thái phiên (stateful session) khi LLM trả lời chậm thế nào?"

**Cách đối đáp:**
> "Câu hỏi chuẩn quá bác ạ. Hiện tại bản PoC đang chạy đồng bộ (synchronous) nên nếu gặp tác vụ Agent suy luận mất 30–60 giây sẽ bị nghẽn ngay. Hướng tiếp theo bắt buộc phải chuyển sang cơ chế bất đồng bộ (Async Webhook / Event-driven Queue) kèm trạng thái phiên (PENDING → NEGOTIATING → VERIFIED). Bác có kinh nghiệm thiết kế luồng này trên Python hoặc Go thì ghé qua GitHub mở giúp mình 1 Issue định hướng kiến trúc nhé!"

---

### Tình huống C — Bình luận ủng hộ và muốn tham gia:
*Ý kiến tích cực:* "Ý tưởng thú vị đấy, mình biết Python cơ bản thì phụ được gì không?"

**Cách đối đáp:**
> "Quá tuyệt vời bác ơi! Mình đã tạo sẵn 3 đầu việc rất gọn trong mục Issues trên GitHub (gắn nhãn good first issue), trong đó có việc viết bộ Unit Test cơ bản bằng thư viện unittest mặc định của Python cho file hello_bridge.py (Issue #3). Bác ghé qua repo nhận giúp mình Issue đó nhé, cảm ơn bác rất nhiều!"
