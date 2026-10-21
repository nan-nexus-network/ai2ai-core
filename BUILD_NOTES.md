# Ghi Chú Về Cách Dự Án Này Được Xây Dựng (Build Notes)

* **Phiên bản:** v0.1 · **Ngày:** 21/10/2026
* **Giấy phép tài liệu:** CC-BY 4.0 (mã nguồn đính kèm: Apache 2.0)
* **Mục đích:** công khai cách dự án này được tạo ra, để bất kỳ ai đến đây đều có thể tự kiểm chứng, chứ không phải tin lời chúng tôi.

---

## 1. Tóm tắt trong một dòng

**Một người, một ngày, 0 đồng, có dùng trợ lý AI, toàn bộ mã nguồn mở theo Apache 2.0, và lịch sử Git công khai hoàn toàn.**

| Con số | Giá trị |
|:--|:--|
| Thời gian xây dựng | **1 ngày** (21/10/2026, 12:55 đến 18:56, giờ Việt Nam) |
| Số commit | **25** |
| Số file trong kho | **60** |
| Chi phí tiền mặt | **0 đồng** |
| Người viết mã | **1** (không phải lập trình viên chuyên nghiệp) |
| Phụ thuộc ngoài | **0** (100% thư viện chuẩn Python) |
| Demo chạy được | **2** |
| Bộ kiểm thử tự động | **10** test |
| Ma trận CI | **8** job (3 hệ điều hành × 3 phiên bản Python) |
| Ngôn ngữ trang chủ | **3** (Việt / Anh / Trung) |

---

## 2. 0 đồng nghĩa là gì, cụ thể

Chúng tôi **không nhận** một đồng nào từ bất kỳ ai, và chúng tôi **không chi** một đồng nào cho hạ tầng hay công cụ:

| Hạng mục | Chi phí |
|:---|:---|
| Máy tính | Tài sản cá nhân của người khởi xướng, không tính chi phí dự án |
| Mã nguồn | 0 đồng, Apache 2.0 |
| Tài liệu | 0 đồng, CC-BY 4.0 |
| Lưu trữ mã | Tầng miễn phí GitHub cho kho công khai |
| Trang tĩnh | Tầng miễn phí Cloudflare Workers, dùng địa chỉ `*.workers.dev` (không mua tên miền riêng) |
| Hộp thư liên hệ | Tầng miễn phí Proton Mail |
| Trình biên dịch, trình soạn thảo, công cụ AI | Các gói miễn phí đã có sẵn |

**Chúng tôi không có tài khoản nhận quyền đăng ký trả phí ở bất kỳ nơi nào.** Đó là lý do kho này không có nút "Sponsor": chưa có tài khoản nào để bật. Nếu sau này có ai muốn tài trợ, chúng tôi sẽ công khai và ghi rõ trong [CHANGELOG.md](CHANGELOG.md).

---

## 3. AI được dùng ở đâu, và không được dùng ở đâu

**Được dùng:** phác thảo cấu trúc tài liệu, biên tập văn phong, viết và gỡ lỗi mã PoC, dựng bộ kiểm thử, và phân tích tài liệu pháp lý quốc tế để trích dẫn.

**Không được dùng để:** tự quyết định luận điểm, tự khẳng định tính đúng của thiết kế, hoặc thay thế kiểm chứng của người đọc.

**Sự hỗ trợ của AI không chứng minh thiết kế đúng, không làm mã an toàn, và không có nghĩa giao thức nào đã được triển khai.** Mọi luận điểm trong [White Paper](docs/WHITEPAPER_VN_AI_BRIDGE.md) đều là luận điểm để **phản biện**, không phải kết luận đã được kiểm chứng. Vì vậy chúng tôi đã công khai sẵn [mẫu issue về chữ ký số Ed25519](.github/ISSUE_TEMPLATE/ISSUE_2_CRYPTOGRAPHY_ED25519.md) và một bộ câu hỏi mở trong Chương 6 của tài liệu: **đó là những chỗ chúng tôi biết là chưa xong, và chúng tôi nói trước thay vì đợi người khác phát hiện.**

---

## 4. Vì sao toàn bộ 25 commit đều có cùng một tác giả và cùng một ngày

Đây là điều một người review cẩn thận sẽ nhận ra và đáng để trả lời thẳng.

**Trước khi công bố, lịch sử Git đã được viết lại đúng một lần.** Mục đích là gỡ khỏi lịch sử:

- 2 tài liệu nội bộ từng được commit nhầm (một kế hoạch thực thi nội bộ và một báo cáo kiểm định nội bộ), vốn đã nằm trong `.gitignore` nhưng lịch sử Git là bất biến nên chúng vẫn tồn tại trong commit đầu tiên;
- mọi dấu vết đường dẫn ổ cứng máy tính cá nhân (`C:\NAN_DEV\...`) trong nội dung các commit cũ;
- mọi dấu vết định danh cá nhân và pháp nhân.

**Hệ quả trực tiếp:** vì toàn bộ nội dung được viết lại trong một lần, mọi commit hiện nay mang cùng tác giả `NAN AI2AI <nan_ai2ai@proton.me>` và cùng một mốc ngày. **Đây là hệ quả của việc dọn lịch sử, không phải lịch sử được dựng lên.** Chúng tôi chọn nói rõ điều này thay vì để bạn phải tự suy đoán.

Để tự kiểm chứng, hãy xem commit đầu tiên:

```bash
git log --reverse --format="%h %an %ad %s" | head -1
git ls-tree -r --name-only $(git rev-list --max-parents=0 HEAD)
```

Không có tài liệu nội bộ nào trong cây commit đầu tiên, và toàn bộ mã nguồn đều truy vết được về thời điểm bắt đầu.

---

## 5. Những gì chúng tôi đã kiểm tra trước khi công bố

| Kiểm tra | Kết quả |
|:---|:---|
| Quét secret trong **toàn bộ** lịch sử (mẫu AWS, GitHub token, OpenAI, Slack, PEM) | 0 phát hiện |
| Quét đường dẫn máy trong toàn bộ lịch sử | 0 phát hiện |
| Quét tên người và tên pháp nhân trong toàn bộ lịch sử | 0 phát hiện |
| `python -m unittest discover -s tests` | 10/10 PASS |
| Demo 1 và Demo 2 | exit 0, kể cả khi mô phỏng console Windows mã hóa `cp1252` |
| `python scripts/license_gate.py` | PASS, mọi file nguồn có SPDX header |
| Ma trận CI | 8 job trên Ubuntu, macOS, Windows × Python 3.8 / 3.10 / 3.12 |
| Quét bí mật trong CI | TruffleHog (`--only-verified`) chạy trên mỗi lần push |
| Kiểm tra giấy phép phụ thuộc | `scancode-toolkit` trong workflow `license.yml` |
| Em-dash (dấu gạch dài) | **README, trang chủ và file này: 0.** Tài liệu quy trình nội bộ (kế hoạch ra mắt, bộ phòng thủ truyền thông, quản trị) vẫn dùng em-dash làm dấu phân cách. White Paper còn **đúng 1 chỗ**: trích dẫn nguyên văn tiêu đề chuẩn GB/Z 185-2026 của Trung Quốc, và chúng tôi không sửa tên riêng của một văn bản chính thức, kể cả khi điều đó để lại một dấu gạch dài. |
| Tính nhất quán thuật ngữ "Protocol" so với [ADR-001](docs/ADR_001.md) | Không còn chỗ nào tự gọi dự án là Protocol |

---

## 6. Điều chúng tôi chưa làm được

Nói thẳng để mọi người khỏi phải hỏi:

- **Chưa có chữ ký số.** Biên nhận SHA-256 chỉ chứng minh tính toàn vẹn dữ liệu, **không** xác thực danh tính tác tử. Mẫu issue [Ed25519](.github/ISSUE_TEMPLATE/ISSUE_2_CRYPTOGRAPHY_ED25519.md) mô tả đường đi.
- **Chưa có tầng đàm phán thật.** Bộ lọc trong Demo là so khớp chuỗi tĩnh, **không phải** biện pháp bảo mật.
- **Chưa có bất kỳ triển khai production nào.** Đây là hộp cát thử nghiệm cục bộ.
- **Chưa có kiểm thử tương thích chéo.** Ma trận CI chạy trên 3 hệ điều hành nhưng chưa có hệ thống kiểm thử phân tán.
- **Chưa được ai bên ngoài xác nhận.** Chúng tôi công khai trước, để bạn kiểm chứng, không phải để bạn tin.

---

## 7. Lời kêu gọi

Nếu bạn đọc đến đây và thấy một chỗ sai, hãy mở một issue. Nếu bạn nghĩ cả hướng đi của dự án này là sai, hãy nói thẳng ở [Chương 6 của White Paper](docs/WHITEPAPER_VN_AI_BRIDGE.md) hoặc trong phần thảo luận. Một phản biện đúng là giá trị nhất mà chúng tôi có thể nhận được từ một dự án không nhận tiền.

**Tiêu chí để chúng tôi dừng lại:** Nếu sau 12 tháng, giao thức này không được cộng đồng đón nhận hoặc chứng minh được giá trị thực tiễn, chúng tôi sẽ công khai dừng dự án để không lãng phí nguồn lực xã hội.

---

*Xem thêm: [README.md](README.md) · [White Paper](docs/WHITEPAPER_VN_AI_BRIDGE.md) · [Press Kit](docs/PRESS_KIT.md) · [Kế hoạch công khai](docs/public_launch/01_LAUNCH_PLAN.md) · [Changelog](CHANGELOG.md)*
