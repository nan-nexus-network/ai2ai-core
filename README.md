# NAN AI2AI-SI2SI: Hộp Cát Thử Nghiệm Cầu Nối Tham Chiếu AI (Open Reference Bridge Sandbox)

> **⚠️ PROOF OF CONCEPT (PoC): DO NOT USE IN PRODUCTION**<br>
> Mã nguồn chỉ minh họa một luồng cục bộ với dữ liệu mẫu. Bộ lọc chuỗi tĩnh không phải biện pháp bảo mật; SHA-256 trong biên nhận không xác thực danh tính, chữ ký hay việc thực thi từ xa. Chưa có transport giữa các Agent, xác thực, phân quyền hoặc kiểm chứng độc lập.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Docs: CC-BY 4.0](https://img.shields.io/badge/Whitepaper-CC--BY_4.0-green.svg)](docs/WHITEPAPER_VN_AI_BRIDGE.md)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B_Stdlib-brightgreen.svg)](examples/01-hello-agent/hello_bridge.py)
[![Code: PoC v0.1](https://img.shields.io/badge/Code-PoC_v0.1-orange.svg)](examples/01-hello-agent/hello_bridge.py)
[![White Paper: v0.4-draft](https://img.shields.io/badge/Whitepaper-v0.4--draft-blue.svg)](docs/WHITEPAPER_VN_AI_BRIDGE.md)
[![CI](https://github.com/nan-nexus-network/ai2ai-core/actions/workflows/ci.yml/badge.svg)](https://github.com/nan-nexus-network/ai2ai-core/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/nan-nexus-network/ai2ai-core)](https://github.com/nan-nexus-network/ai2ai-core/releases)

> 📖 **Cách dự án này được xây dựng:** [BUILD_NOTES.md](BUILD_NOTES.md). 0 đồng, có dùng trợ lý AI, toàn bộ lịch sử viết trong một ngày.

> ⚠️ **Định vị:** Đây là **Open Reference Framework** (Khung tham chiếu mở), **chưa phải** Protocol (Giao thức) theo nghĩa được chuẩn hóa quốc tế. Xem lý do tại [ADR-001](docs/ADR_001.md). Điều kiện để nâng cấp lên Protocol được ghi rõ trong ADR.

> **"Việt Nam không nhất thiết phải đua xây dựng các siêu mô hình tỷ đô, nhưng liệu chúng ta có thể đóng vai trò 'Cầu nối Tham Chiếu' (Reference Bridge) giúp các hệ sinh thái AI phân mảnh liên vận với nhau?"**

---

## 🔍 Tuyên Bố Minh Bạch (Transparency First)

Trước khi bạn đọc mã nguồn hoặc tài liệu trong kho lưu trữ này, chúng tôi xin công khai rõ:

**Mục đích của dự án:** Dự án NAN AI2AI được xây dựng với mục đích đóng góp cho Kỷ nguyên AI Việt Nam. Chúng tôi không tìm kiếm lợi nhuận từ việc bán dự án hay gọi vốn đầu tư.

1. **Bản chất dự án:** Đây là một hộp cát thử nghiệm kỹ thuật (Open Sandbox) đi kèm với [Tài liệu thảo luận mở: Việt Nam như cầu nối trong nền kinh tế AI2AI](docs/WHITEPAPER_VN_AI_BRIDGE.md). Đây **chưa phải** là một giao thức hoàn chỉnh sẵn sàng cho môi trường thương mại.
2. **Về người khởi xướng & Công cụ AI:** Người khởi xướng dự án làm việc trong mảng nghiên cứu và kết nối, không phải là kỹ sư lập trình chuyên nghiệp. Tài liệu và mã nguồn mẫu (PoC) được phác thảo với sự hỗ trợ của AI (Claude) nhằm minh họa trực quan bài toán để mời cộng đồng kỹ sư kiểm tra, phản biện và cải thiện.
3. **Ba cam kết bất biến:**
   - **Không xin tiền, không gọi vốn, không phát hành token, không bán khóa học.**
   - **Minh bạch tuyệt đối về giới hạn kỹ thuật.**
   - **Mọi mã nguồn đã mở dưới chuẩn Apache 2.0 sẽ không bao giờ bị rút lại.**
4. **Về tính đại diện:** Sáng kiến này **hoàn toàn không đại diện cho cộng đồng AI Việt Nam**. Đây là một thử nghiệm độc lập ở quy mô nhỏ; mọi luận điểm trong [Tài liệu thảo luận](docs/WHITEPAPER_VN_AI_BRIDGE.md) đều được trình bày như **câu hỏi mở**, không phải kết luận.
5. **Về giới hạn kỹ thuật:** Chúng tôi liệt kê **từng giới hạn đã biết** — kể cả những giới hạn của phần mã vừa được viết — tại [ARCHITECTURE.md](ARCHITECTURE.md), trong bảng giới hạn của [ADR-001](docs/ADR_001.md), và trong [ADR-002](docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md). Phần chữ ký số mới là **bản tham chiếu phục vụ học tập**, chưa phải mã production: Ed25519 thuần Python **không constant-time**, và mô hình neo tin cậy TOFU **không** chống được tấn công MITM ở lần tiếp xúc đầu tiên.

### Tại sao tôi dùng AI?

Tôi dùng AI (Claude) để hỗ trợ phác thảo tài liệu và mã PoC vì tôi không phải kỹ sư phần mềm chuyên nghiệp. Tôi đưa ra vấn đề muốn thảo luận, dùng bản nháp để làm rõ ý tưởng, rồi công khai giới hạn để cộng đồng có thể phản biện, kiểm tra và viết lại. Sự hỗ trợ của AI không chứng minh thiết kế đúng, mã an toàn hay giao thức đã được triển khai; PoC hiện chỉ là minh họa ban đầu. **Chi tiết đầy đủ về quá trình, chi phí, công cụ đã dùng và những gì đã bị gỡ khỏi lịch sử: [BUILD_NOTES.md](BUILD_NOTES.md).**

---

## ⚡ Chạy Thử Nghiệm Trong 60 Giây (Zero Dependencies)

> 📌 **Trạng thái phiên bản:** nhánh `main` đang phát triển **v0.2** (biên nhận có chữ ký + bộ kiểm tra cấu trúc theo allowlist schema). Bản phát hành ổn định vẫn là **v0.1.0**. Chi tiết các quyết định kiến trúc: [ADR-002](docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md).

Bản mẫu `hello_bridge.py` sử dụng 100% thư viện mặc định của Python (tương thích từ Python 3.8 trở lên), không cần cài đặt bất kỳ gói phụ thuộc nào (`pip install`).

Xem [ARCHITECTURE.md](ARCHITECTURE.md) để biết luồng hiện có và những lớp nào **mới chỉ là ý tưởng**.

```bash
git clone https://github.com/nan-nexus-network/ai2ai-core.git
cd ai2ai-core
python examples/01-hello-agent/hello_bridge.py
```

### Kịch bản mô phỏng trong 60 giây:
1. **Agent Hệ sinh thái A (chuẩn MCP-style)** phát một gói tin yêu cầu dịch vụ logistics ASEAN.
2. **Node Cầu nối (ProtocolBridgeNode)** kiểm tra gói tin qua **hai lớp**: (Lớp 1) *allowlist schema* — kiểm tra kiểu dữ liệu, độ dài, miền giá trị và **từ chối mọi trường không nằm trong schema**; (Lớp 2) *so khớp một số chuỗi tĩnh* như lớp phòng thủ thứ hai. Lớp 1 là **subset của JSON Schema Draft 2020-12, tự viết bằng thư viện chuẩn** — **không phải** bản triển khai đầy đủ của Draft 2020-12, và vẫn là kiểm tra minh họa, không phải biện pháp bảo mật. Xem [ADR-002](docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md).
3. **Chuyển đổi ngữ nghĩa:** Dịch từ cấu trúc gọi công cụ (`tool_call`) sang cấu trúc giao việc liên vận (`standardized_task` kiểu A2A).
4. **Tạo biên nhận demo:** Tính digest SHA-256 từ dữ liệu mẫu và phản hồi mô phỏng; digest không xác thực danh tính, nguồn gốc hoặc việc thực thi.

### Demo 2: Agent-to-Agent Chat (P2P)
Dành cho các cá nhân muốn thử nghiệm kết nối AI của mình với AI của người khác. Zero dependencies, chạy trong 60 giây.
```bash
python examples/02-agent-to-agent-chat/agent_chat.py
```
*(Mô phỏng cảnh Alice gửi yêu cầu tìm nhà cung cấp qua NAN Bridge, Bob xử lý và trả kết quả kèm Biên nhận SHA-256).*

> ⚠️ **Lưu ý trung thực:** Demo 2 **không** gọi lớp kiểm tra cấu trúc của Demo 1 — đây là **hai hiện thực bridge độc lập chưa được hợp nhất**, một việc đã đưa vào backlog. Chúng tôi nói rõ điều này thay vì để người đọc tự phát hiện.

### Demo 3: Biên nhận có chữ ký (v0.2)
Bản nhận `nan-receipt/v1`: **chỉ bên thực thi ký** (Ed25519), nên **một bên thứ ba có thể xác minh mà không cần tin vào Bridge**. Zero dependencies, chạy trong 60 giây.
```bash
python examples/03-signed-receipt/signed_receipt_demo.py
```
*(Demo cho thấy: bên thứ ba ghim khoá công khai theo mô hình TOFU, kiểm tra chữ ký, và **từ chối** biên nhận bị sửa, bị hết hạn, hoặc bị khoá lạ. Xem [ADR-002](docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md) để biết vì sao chọn phạm vi ký này.)*

---

## 📄 Tài Liệu Thảo Luận Mở (White Paper v0.4-draft)

- **Đọc trực tiếp bản Markdown:** [docs/WHITEPAPER_VN_AI_BRIDGE.md](docs/WHITEPAPER_VN_AI_BRIDGE.md)
- **Tải bản PDF đầy đủ (kèm Tóm tắt 1 trang cho người bận rộn):** [GitHub Releases](https://github.com/nan-nexus-network/ai2ai-core/releases)
- [ADR-001: Định vị Framework vs Protocol](docs/ADR_001.md)
- [ADR-002: Biên nhận có chữ ký, mô hình neo tin cậy, và bộ kiểm tra cấu trúc](docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md)
- [Media Kit dành cho báo chí](docs/PRESS_KIT.md)

---

## Lời mời từ người khởi xướng

Tôi không phải là một kỹ sư phần mềm chuyên nghiệp. Tôi chỉ có kiến thức tin học cơ bản từ thời phổ thông. Những dòng code ban đầu trong dự án này được tạo ra với sự hỗ trợ của AI. Chúng còn sơ khai, chưa hoàn thiện và cần được những người có chuyên môn kiểm tra, phản biện và phát triển thêm.

Tôi không giấu điều đó.

Tôi bắt đầu NAN AI2AI từ một câu hỏi lớn hơn những dòng code: **Làm thế nào để các hệ thống AI và AI Agent có thể kết nối, trao đổi năng lực và hợp tác với nhau một cách đáng tin cậy, an toàn và có thể kiểm chứng, xuyên qua những hệ sinh thái công nghệ khác nhau?**

Tôi tin rằng đây là một bài toán đáng để người Việt Nam tham gia giải quyết, vừa với tư cách người sử dụng công nghệ, vừa với tư cách những người góp phần xây dựng các lớp kết nối, tiêu chuẩn và hạ tầng cho nền kinh tế AI.

Tôi có ý tưởng, định hướng và khát vọng đó. Tôi đã sử dụng AI để phác thảo kiến trúc và xây dựng những nguyên mẫu kỹ thuật ban đầu. Nhưng tôi hiểu rằng một ý tưởng không tự trở thành tiêu chuẩn, và một nguyên mẫu không tự trở thành sản phẩm đáng tin cậy. Tất cả phải được kiểm chứng bằng kỹ thuật, đánh giá độc lập và kết quả thực tế.

**Đó là lý do tôi mở dự án này.**

Tôi mong muốn được kết nối với các kỹ sư phần mềm, chuyên gia kiến trúc hệ thống, chuyên gia bảo mật, nhà nghiên cứu và những người thực sự quan tâm đến tương lai của AI.

Bạn có thể phản biện kiến trúc, kiểm tra giả định, thiết kế lại schema, cải thiện cơ chế xác thực, bổ sung chữ ký số, xây dựng các bài kiểm thử hoặc đề xuất một hướng tiếp cận tốt hơn. Nếu nền tảng hiện tại chưa phù hợp, chúng ta có thể viết lại. Nếu một giả định không đúng, chúng ta cần đủ dũng khí để sửa nó.

Tôi không mở dự án này để chứng minh rằng mình biết viết code. Tôi mở nó để một ý tưởng có cơ hội được thử thách, cải thiện và phát triển vượt xa khả năng của một cá nhân.

**Bạn không cần đến đây để làm việc cho tôi. Bạn có thể đến đây để cùng xây dựng một nền tảng mở, nơi đóng góp được ghi nhận, quyết định kỹ thuật được thảo luận minh bạch và giá trị được tạo ra từ sự hợp tác.**

NAN AI2AI chưa tuyên bố mình đã tạo ra một tiêu chuẩn hoàn chỉnh. Chúng tôi bắt đầu bằng những nguyên mẫu, câu hỏi mở và các thử nghiệm có thể kiểm chứng. Con đường phía trước cần sự phản biện nghiêm túc và đóng góp của cộng đồng.

Nếu bạn cho rằng bài toán này đáng giải quyết, hãy cùng chúng tôi bắt đầu từ những việc nhỏ nhất: một vấn đề được xác định rõ, một bài kiểm thử có thể tái hiện, một đề xuất kỹ thuật có căn cứ hoặc một dòng code tốt hơn.

**Một người có thể khởi xướng ý tưởng. Nhưng để biến ý tưởng thành hạ tầng có giá trị, chúng ta cần cùng nhau xây dựng.**

---

## 🛠 Cách Tham Gia Phản Biện & Đóng Góp

Chúng tôi cần sự phản biện thẳng thắn của bạn hơn là những lời khen:
- Mở một [GitHub Issue](https://github.com/nan-nexus-network/ai2ai-core/issues) để chỉ ra lỗ hổng trong lập luận hoặc trong code PoC.
- Nhận một đầu việc nhỏ tại mục nhãn `good first issue` (xem hướng dẫn tại [CONTRIBUTING.md](CONTRIBUTING.md)).
- Xem chính sách nhãn hiệu tại [TRADEMARK.md](TRADEMARK.md) và cam kết bàn giao dự án nếu dừng hoạt động tại [HANDOVER.md](HANDOVER.md).

**Liên hệ:** nan_ai2ai@proton.me | **Cổng thông tin:** https://nan-ai2ai.nexusasianetwork.workers.dev

### 🌐 Mạng Lưới Kênh Chính Thức
* **Website:** https://nan-ai2ai.nexusasianetwork.workers.dev
* **Email:** [nan_ai2ai@proton.me](mailto:nan_ai2ai@proton.me)
* **LinkedIn:** https://www.linkedin.com/in/nan-ai2ai-b02b67365/
* **Facebook:** https://www.facebook.com/profile.php?id=61595651371198
* **X (Twitter):** https://x.com/Nan_ai2ai_vn
* **Zalo Group:** https://zalo.me/g/h0cbluccgocfud9fmih4
* **Telegram:** https://t.me/+87ARJ1e1NUA0ZDQ1

---

## 📁 Kế Hoạch Công Khai & Quản Trị

| Tài liệu | Nội dung |
| :--- | :--- |
| [docs/public_launch/](docs/public_launch/) | **Bộ kế hoạch công khai đầy đủ**: kế hoạch ra mắt, quản trị, đo lường, sổ rủi ro, checklist phát hành |
| [GOVERNANCE.md](GOVERNANCE.md) | Cách ra quyết định, phân quyền, và **cách xử lý bất đồng** (không có deadlock) |
| [SECURITY.md](SECURITY.md) | Công bố lỗ hổng bảo mật |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Nguyên tắc ứng xử cộng đồng |
| [ROADMAP.md](ROADMAP.md) | Lộ trình công khai |
| [CHANGELOG.md](CHANGELOG.md) | Nhật ký phát hành |

---

## 💰 Câu Chuyện 0 Đồng (The Zero-Budget Story)

Chúng tôi khởi đầu với 0 đồng. Tên miền miễn phí, hạ tầng miễn phí, và code được hỗ trợ bởi AI. Chúng tôi tin rằng một ý tưởng lớn không cần một ngân sách lớn để bắt đầu. Nếu chúng tôi làm được, các bạn trẻ Việt Nam cũng có thể làm được.
