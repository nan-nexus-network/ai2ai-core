# NAN AI2AI-SI2SI: Hộp Cát Thử Nghiệm Cầu Nối Giao Thức AI (Open Protocol Bridge Sandbox)

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
2. **Về người khởi xướng & Công cụ AI:** Người khởi xướng dự án làm việc trong mảng nghiên cứu và kết nối, không phải là kỹ sư lập trình chuyên nghiệp. Tài liệu và mã nguồn mẫu (PoC) được phác thảo với sự hỗ trợ của AI (Claude) nhằm minh họa trực quan bài toán để mời các kỹ sư thực thụ kiểm chứng, bắt lỗi và viết lại.
3. **Ba cam kết bất biến:**
   * **Không xin tiền, không gọi vốn, không phát hành token, không bán khóa học.**
   * **Minh bạch tuyệt đối về giới hạn kỹ thuật.**
   * **Mọi mã nguồn đã mở dưới chuẩn Apache 2.0 sẽ không bao giờ bị rút lại.**
4. **Về tính đại diện:** Sáng kiến này **hoàn toàn không đại diện cho cộng đồng AI Việt Nam**. Đây là một thử nghiệm độc lập ở quy mô nhỏ; mọi luận điểm trong [Tài liệu thảo luận](docs/WHITEPAPER_VN_AI_BRIDGE.md) đều được trình bày như **câu hỏi mở**, không phải kết luận.

---

## ⚡ Chạy Thử Nghiệm Trong 60 Giây (Zero Dependencies)

Bản mẫu `hello_bridge.py` sử dụng 100% thư viện mặc định của Python (tương thích từ Python 3.8 trở lên), không cần cài đặt bất kỳ gói phụ thuộc nào (`pip install`).

```bash
git clone https://github.com/nan-nexus-network/ai2ai-core.git
cd ai2ai-core
python examples/01-hello-agent/hello_bridge.py
```

### Kịch bản mô phỏng trong 60 giây:
1. **Agent Hệ sinh thái A (chuẩn MCP-style)** phát một gói tin yêu cầu dịch vụ logistics ASEAN.
2. **Node Cầu nối (ProtocolBridgeNode)** kiểm tra hợp đồng dữ liệu (Schema Contract) và quét an toàn trên toàn bộ gói tin.
3. **Chuyển đổi ngữ nghĩa:** Dịch từ cấu trúc gọi công cụ (`tool_call`) sang cấu trúc giao việc liên vận (`standardized_task` kiểu A2A).
4. **Cấp biên nhận xác thực:** Băm toàn bộ đề bài và kết quả trả về bằng SHA-256 để tạo biên nhận kiểm chứng (Verification Receipt).

---

## 📄 Tài Liệu Thảo Luận Mở (White Paper v0.4-draft)

* **Đọc trực tiếp bản Markdown:** [docs/WHITEPAPER_VN_AI_BRIDGE.md](docs/WHITEPAPER_VN_AI_BRIDGE.md)
* **Tải bản PDF đầy đủ (kèm Tóm tắt 1 trang cho người bận rộn):** [GitHub Releases](https://github.com/nan-nexus-network/ai2ai-core/releases)

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
