# NAN AI2AI-SI2SI: Hộp Cát Thử Nghiệm Cầu Nối Giao Thức AI (Open Protocol Bridge Sandbox)

> **⚠️ PROOF OF CONCEPT (PoC) — DO NOT USE IN PRODUCTION**<br>
> Mã nguồn chỉ minh họa một luồng cục bộ với dữ liệu mẫu. Bộ lọc chuỗi tĩnh không phải biện pháp bảo mật; SHA-256 trong biên nhận không xác thực danh tính, chữ ký hay việc thực thi từ xa. Chưa có transport giữa các Agent, xác thực, phân quyền hoặc kiểm chứng độc lập.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Docs: CC-BY 4.0](https://img.shields.io/badge/Whitepaper-CC--BY_4.0-green.svg)](docs/WHITEPAPER_VN_AI_BRIDGE.md)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B_Stdlib-brightgreen.svg)](examples/01-hello-agent/hello_bridge.py)
[![Code: PoC v0.1](https://img.shields.io/badge/Code-PoC_v0.1-orange.svg)]()
[![White Paper: v0.4-draft](https://img.shields.io/badge/Whitepaper-v0.4--draft-blue.svg)]()

> **"Việt Nam không nhất thiết phải đua xây dựng các siêu mô hình tỷ đô, nhưng liệu chúng ta có thể đóng vai trò 'Cầu nối Giao thức' (Protocol Bridge) giúp các hệ sinh thái AI phân mảnh liên vận với nhau?"**

---

## 🔍 Tuyên Bố Minh Bạch (Transparency First)

Trước khi bạn đọc mã nguồn hoặc tài liệu trong kho lưu trữ này, chúng tôi xin công khai rõ:

1. **Bản chất dự án:** Đây là một hộp cát thử nghiệm kỹ thuật (Open Sandbox) đi kèm với [Tài liệu thảo luận mở: Việt Nam như cầu nối trong nền kinh tế AI2AI](docs/WHITEPAPER_VN_AI_BRIDGE.md). Đây **chưa phải** là một giao thức hoàn chỉnh sẵn sàng cho môi trường thương mại.
2. **Về người khởi xướng & Công cụ AI:** Người khởi xướng dự án làm việc trong mảng nghiên cứu và kết nối, không phải là kỹ sư lập trình chuyên nghiệp. Tài liệu và mã nguồn mẫu (PoC) được phác thảo với sự hỗ trợ của AI (Claude) nhằm minh họa trực quan bài toán để mời cộng đồng kỹ sư kiểm tra, phản biện và cải thiện.
3. **Ba cam kết bất biến:**
   * **Không xin tiền, không gọi vốn, không phát hành token, không bán khóa học.**
   * **Minh bạch tuyệt đối về giới hạn kỹ thuật.**
   * **Mọi mã nguồn đã mở dưới chuẩn Apache 2.0 sẽ không bao giờ bị rút lại.**
4. **Về tính đại diện:** Sáng kiến này **hoàn toàn không đại diện cho cộng đồng AI Việt Nam**. Đây là một thử nghiệm độc lập ở quy mô nhỏ; mọi luận điểm trong [Tài liệu thảo luận](docs/WHITEPAPER_VN_AI_BRIDGE.md) đều được trình bày như **câu hỏi mở**, không phải kết luận.

### Tại sao tôi dùng AI?

Tôi dùng AI (Claude) để hỗ trợ phác thảo tài liệu và mã PoC vì tôi không phải kỹ sư phần mềm chuyên nghiệp. Tôi đưa ra vấn đề muốn thảo luận, dùng bản nháp để làm rõ ý tưởng, rồi công khai giới hạn để cộng đồng có thể phản biện, kiểm tra và viết lại. Sự hỗ trợ của AI không chứng minh thiết kế đúng, mã an toàn hay giao thức đã được triển khai; PoC hiện chỉ là minh họa ban đầu.

---

## ⚡ Chạy Thử Nghiệm Trong 60 Giây (Zero Dependencies)

Bản mẫu `hello_bridge.py` sử dụng 100% thư viện mặc định của Python (tương thích từ Python 3.8 trở lên), không cần cài đặt bất kỳ gói phụ thuộc nào (`pip install`).

Xem [ARCHITECTURE.md](ARCHITECTURE.md) để biết luồng hiện có và các lớp mới chỉ mang tính khái niệm.

```bash
git clone https://github.com/nan-nexus-network/ai2ai-core.git
cd ai2ai-core
python examples/01-hello-agent/hello_bridge.py
```

### Kịch bản mô phỏng trong 60 giây:
1. **Agent Hệ sinh thái A (chuẩn MCP-style)** phát một gói tin yêu cầu dịch vụ logistics ASEAN.
2. **Node Cầu nối (ProtocolBridgeNode)** kiểm tra một số trường bắt buộc và so khớp một số chuỗi tĩnh trong gói tin; đây là kiểm tra minh họa, không phải biện pháp bảo mật.
3. **Chuyển đổi ngữ nghĩa:** Dịch từ cấu trúc gọi công cụ (`tool_call`) sang cấu trúc giao việc liên vận (`standardized_task` kiểu A2A).
4. **Tạo biên nhận demo:** Tính digest SHA-256 từ dữ liệu mẫu và phản hồi mô phỏng; digest không xác thực danh tính, nguồn gốc hoặc việc thực thi.

---

## 📄 Tài Liệu Thảo Luận Mở (White Paper v0.4-draft)

* **Đọc trực tiếp bản Markdown:** [docs/WHITEPAPER_VN_AI_BRIDGE.md](docs/WHITEPAPER_VN_AI_BRIDGE.md)
* **Tải bản PDF đầy đủ (kèm Tóm tắt 1 trang cho người bận rộn):** [GitHub Releases](https://github.com/nan-nexus-network/ai2ai-core/releases)

---

## Lời mời từ người khởi xướng

Tôi không phải là một kỹ sư phần mềm chuyên nghiệp. Tôi chỉ có kiến thức tin học cơ bản từ thời phổ thông. Những dòng code ban đầu trong dự án này được tạo ra với sự hỗ trợ của AI. Chúng còn sơ khai, chưa hoàn thiện và cần được những người có chuyên môn kiểm tra, phản biện và phát triển thêm.

Tôi không giấu điều đó.

Tôi bắt đầu NAN AI2AI từ một câu hỏi lớn hơn những dòng code: **Làm thế nào để các hệ thống AI và AI Agent có thể kết nối, trao đổi năng lực và hợp tác với nhau một cách đáng tin cậy, an toàn và có thể kiểm chứng — xuyên qua những hệ sinh thái công nghệ khác nhau?**

Tôi tin rằng đây là một bài toán đáng để người Việt Nam tham gia giải quyết, không chỉ với tư cách người sử dụng công nghệ, mà còn với tư cách những người góp phần xây dựng các lớp kết nối, tiêu chuẩn và hạ tầng cho nền kinh tế AI.

Tôi có ý tưởng, định hướng và khát vọng đó. Tôi đã sử dụng AI để phác thảo kiến trúc và xây dựng những nguyên mẫu kỹ thuật ban đầu. Nhưng tôi hiểu rằng một ý tưởng không tự trở thành tiêu chuẩn, và một nguyên mẫu không tự trở thành sản phẩm đáng tin cậy. Tất cả phải được kiểm chứng bằng kỹ thuật, đánh giá độc lập và kết quả thực tế.

**Đó là lý do tôi mở dự án này.**

Tôi mong muốn được kết nối với các kỹ sư phần mềm, chuyên gia kiến trúc hệ thống, chuyên gia bảo mật, nhà nghiên cứu và những người thực sự quan tâm đến tương lai của AI.

Bạn có thể phản biện kiến trúc, kiểm tra giả định, thiết kế lại schema, cải thiện cơ chế xác thực, bổ sung chữ ký số, xây dựng các bài kiểm thử hoặc đề xuất một hướng tiếp cận tốt hơn. Nếu nền tảng hiện tại chưa phù hợp, chúng ta có thể viết lại. Nếu một giả định không đúng, chúng ta cần đủ dũng khí để sửa nó.

Tôi không mở dự án này để chứng minh rằng mình biết viết code. Tôi mở nó để một ý tưởng có cơ hội được thử thách, cải thiện và phát triển vượt xa khả năng của một cá nhân.

**Bạn không cần đến đây để làm việc cho tôi. Bạn có thể đến đây để cùng xây dựng một nền tảng mở, nơi đóng góp được ghi nhận, quyết định kỹ thuật được thảo luận minh bạch và giá trị được tạo ra từ sự hợp tác.**

NAN AI2AI chưa tuyên bố mình đã tạo ra một tiêu chuẩn hoàn chỉnh. Chúng tôi bắt đầu bằng những nguyên mẫu, câu hỏi mở và các thử nghiệm có thể kiểm chứng. Con đường phía trước cần sự phản biện nghiêm túc và đóng góp của cộng đồng.

Nếu bạn cho rằng bài toán này đáng giải quyết, hãy cùng chúng tôi bắt đầu từ những việc nhỏ nhất — một vấn đề được xác định rõ, một bài kiểm thử có thể tái hiện, một đề xuất kỹ thuật có căn cứ hoặc một dòng code tốt hơn.

**Một người có thể khởi xướng ý tưởng. Nhưng để biến ý tưởng thành hạ tầng có giá trị, chúng ta cần cùng nhau xây dựng.**

---

## 🛠 Cách Tham Gia Phản Biện & Đóng Góp

Chúng tôi cần sự phản biện thẳng thắn của bạn hơn là những lời khen:
* Mở một [GitHub Issue](https://github.com/nan-nexus-network/ai2ai-core/issues) để chỉ ra lỗ hổng trong lập luận hoặc trong code PoC.
* Nhận một đầu việc nhỏ tại mục nhãn `good first issue` (xem hướng dẫn tại [CONTRIBUTING.md](CONTRIBUTING.md)).
* Xem chính sách nhãn hiệu tại [TRADEMARK.md](TRADEMARK.md) và cam kết bàn giao dự án nếu dừng hoạt động tại [HANDOVER.md](HANDOVER.md).

**Liên hệ:** nan.ai2ai.initiative@proton.me | **Cổng thông tin:** https://nan-ai2ai.pages.dev

---

## 📁 Kế Hoạch Công Khai & Quản Trị

| Tài liệu | Nội dung |
| :--- | :--- |
| [docs/public_launch/](docs/public_launch/) | **Bộ kế hoạch công khai đầy đủ** — kế hoạch ra mắt, quản trị, đo lường, sổ rủi ro, checklist phát hành |
| [GOVERNANCE.md](GOVERNANCE.md) | Cách ra quyết định, phân quyền, và **cách xử lý bất đồng** (không có deadlock) |
| [SECURITY.md](SECURITY.md) | Công bố lỗ hổng bảo mật |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Nguyên tắc ứng xử cộng đồng |
| [ROADMAP.md](ROADMAP.md) | Lộ trình công khai |
| [CHANGELOG.md](CHANGELOG.md) | Nhật ký phát hành |
