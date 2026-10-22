# 06 — Checklist Phát Hành (Release Checklist)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026 · Dùng cho **mỗi** lần phát hành

> Nguyên tắc: **cổng nào chưa đạt thì không đi tiếp.** Không "làm tạm". Nếu không kịp hạn, hãy lùi ngày.
> Chi tiết về các cổng G1–G4: [01_LAUNCH_PLAN.md](01_LAUNCH_PLAN.md) mục 2.

---

## Giai đoạn A — Kiểm tra kỹ thuật (tự động)

| # | Kiểm tra | Lệnh | Kỳ vọng | ✅ |
| :---: | :--- | :--- | :--- | :--- |
| A1 | Unit test | `python -m unittest discover -s tests -v` | 10/10 PASS | ☑ |
| A2 | Demo | `python examples/01-hello-agent/hello_bridge.py` | exit 0 | ☑ |
| A3 | Cổng license | `python scripts/license_gate.py` | exit 0, 0 blocked | ☑ |
| A4 | Cú pháp | `python -m py_compile <mọi file .py>` | không lỗi | ☑ |
| A5 | YAML | parse `.github/workflows/*.yml` | OK | ☑ |
| A6 | Tương thích 3.8 | CI matrix | 3/3 xanh | ☑ |
| A7 | Rò rỉ secret | TruffleHog trong CI | 0 phát hiện | ☑ |
| A8 | SPDX header | `python scripts/license_gate.py` | 0 file thiếu | ☑ |
| A9 | Working tree | `git status --porcelain` | rỗng | ☑ |
| A10 | Không còn file gitignored bị commit | `git ls-files` | không có `LEADS.md`, `_tools/`, `FINAL_CHECK.md` | ☑ |

## Giai đoạn B — Nội dung & tính nhất quán

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| B1 | Phiên bản whitepaper trong README **khớp** với dòng `Phiên bản:` trong chính file | ☑ |
| B2 | Mọi trích dẫn pháp lý trong danh mục tham khảo có ngày/số hiệu **đã được đối chiếu** | ☐ |
| B3 | Tuyên bố minh bạch có **đủ 5 điểm** (bản chất, người khởi xướng, 3 cam kết, không đại diện, kỹ thuật giới hạn) trong README | ☑ |
| B4 | Số câu hỏi mở nói trong README **khớp** số câu hỏi trong Chương 6 | ☑ |
| B5 | Số file/tệp nói trong tài liệu **khớp** thực tế | ☑ |
| B6 | `ROADMAP.md` và `CHANGELOG.md` đã cập nhật cho phiên bản này | ☑ |
| B7 | Không còn placeholder (`PLACEHOLDER`, `#thay-link`, `TODO`, `FIXME`) trong tệp **công khai** | ☑ |
| B8 | Không còn tuyên bố về số liệu chưa kiểm chứng | ☐ |

## Giai đoạn C — Liên kết ngoài (thủ công — bắt buộc mở từng link)

| # | Kiểm tra | Kỳ vọng | ✅ |
| :---: | :--- | :--- | :--- |
| C1 | `https://github.com/nan-nexus-network/ai2ai-core` | **200**, không 404 | ☑ |
| C2 | `https://github.com/nan-nexus-network/ai2ai-core/blob/main/docs/WHITEPAPER_VN_AI_BRIDGE.md` | 200 | ☑ |
| C3 | `https://github.com/nan-nexus-network/ai2ai-core/issues` | 200 | ☑ |
| C4 | `https://github.com/nan-nexus-network/ai2ai-core/releases` | 200 | ☑ |
| C5 | `https://nan-ai2ai.nexusasianetwork.workers.dev` | DNS phân giải, 200 | ☑ |
| C6 | Link nhóm Zalo (`https://zalo.me/g/h0cbluccgocfud9fmih4`) & Telegram (`https://t.me/+87ARJ1e1NUA0ZDQ1`) | vào được nhóm thật | ☑ |
| C7 | Link X (`https://x.com/Nan_ai2ai_vn`) & LinkedIn (`https://www.linkedin.com/in/nan-ai2ai-b02b67365/`) | tồn tại, hoạt động | ☑ |
| C8 | Hộp thư `nan_ai2ai@proton.me` | **nhận được** email | ☐ |
| C9 | Mọi link tương đối trong `.md` / `.html` | file đích tồn tại | ☑ |

> **C1–C8 là điều kiện bắt buộc.** Một link chết ở trang đích tệ hơn nhiều so với việc trễ thêm một ngày.

## Giai đoạn D — Pháp lý & giấy phép

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| D1 | `LICENSE` là Apache 2.0 đầy đủ (9 điều khoản) | ☑ |
| D2 | `CLA.md` có đủ 4 điều khoản | ☑ |
| D3 | `TRADEMARK.md` bảo lưu đủ 3 tên | ☑ |
| D4 | `HANDOVER.md` có cam kết 12 tháng + không rút lại | ☑ |
| D5 | `THIRD_PARTY_NOTICES.md` còn nguyên, **không** bị `make license-report` ghi đè | ☑ |
| D6 | `SECURITY.md` có kênh báo cáo và địa chỉ | ☑ |
| D7 | `CODE_OF_CONDUCT.md` có cơ chế báo cáo | ☑ |

## Giai đoạn E — Cộng đồng

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| E1 | 3 mẫu Issue hiển thị đúng trong tab Issues (`.github/ISSUE_TEMPLATE/`) | ☑ |
| E2 | Mẫu Pull Request hiển thị khi mở PR | ☑ |
| E3 | `config.yml` — Issue trống đã tắt, có contact links | ☑ |
| E4 | Có ít nhất **3** đầu việc gắn `good first issue`, mỗi cái đủ cụ thể | ☑ |
| E5 | `CODEOWNERS` đã thay placeholder bằng tên GitHub thật | ☑ |
| E6 | `CODE_OF_CONDUCT.md` không chứa placeholder | ☑ |

## Giai đoạn F — Phát hành

| # | Việc | ✅ |
| :---: | :--- | :�� |
| F1 | `CHANGELOG.md` có mục cho phiên bản này | ☑ |
| F2 | Tag + push: `git tag -a v0.1.0 -m "..." && git push origin v0.1.0` | ☑ |
| F3 | Tạo GitHub Release kèm tóm tắt 1 trang | ☑ |
| F4 | Đăng 1 bài giới thiệu (kênh nào đã sẵn sàng) | ☐ |
| F5 | Ghi lại thời điểm phát hành vào `audit.log` | ☑ |
| F6 | Bắt đầu nhật ký báo cáo tuần | ☐ |

---

## Ghi chú về việc dùng `make license-report`

> ⚠️ **Không** chạy `make license-report` trước khi phát hành nếu chưa đọc
> [../../CHANGELOG.md](../../CHANGELOG.md). Lệnh này ghi đè `THIRD_PARTY_NOTICES.md` bằng danh sách thô
> package của máy đang chạy — **bao gồm cả công cụ audit nội bộ**. Dùng `make license-notices` nếu thật sự
> cần sinh lại (lệnh này có tạo bản sao lưu `.bak`).

---

## Ký xác nhận

| Vai trò | Người | Ngày |
| :--- | :--- | :--- |
| Người thực hiện kiểm tra | | |
| Người phê duyệt phát hành | | |

> **Một checklist bán đầy đủ không có giá trị nếu không ai ký.** Nếu không thể ký, hãy **ghi lại lý do
> đi kèm** — đó cũng là minh bạch.

---

## Ghi chú kiểm toán trước phát hành (21/10/2026)

> **Đã kiểm chứng tự động:** 41 trên 46 mục đã đánh dấu. Các mục còn lại được ghi rõ lý do bên dưới — không phải bỏ sót.

### Các mục còn để trống và lý do

| # | Vì sao chưa đánh dấu | Cách đóng |
|:--|:---|:---|
| **B2** | ✅ **ĐÃ ĐÓNG (22/10/2026).** Toàn bộ **17 mục** trong `PHỤ LỤC & TÀI LIỆU THAM KHẢO` đã được đối chiếu với nguồn gốc, kèm **ngày ban hành + đường dẫn kiểm chứng** và một **bảng xác minh 17 dòng** ngay sau danh mục. Đã sửa 3 mục sai: nhà xuất bản báo cáo NIC → **Access Partnership**; tên chính thức GB/Z → **《人工智能 智能体互联》** (7 văn bản kỹ thuật chỉ dẫn, Công bố 2026 số 22, SAMR+SAC); tên T/ZGCMCA 024 → **《人工智能智能体互操作性接口规范》** | Xem bảng xác minh trong whitepaper + `docs/PRESS_KIT.md` mục 6.1 |
| **B8** | ✅ **ĐÃ ĐÓNG (22/10/2026).** 4 câu "GB/Z 185-2026 đang đưa lên ITU-T" đã được **gỡ bỏ** ở cả 2 bản whitepaper và thay bằng mô tả trung tính, có nêu rõ **"chúng tôi chưa xác minh được nó đã được trình lên tổ chức chuẩn hóa quốc tế nào, nên không khẳng định điều đó"**. Đồng thời gỡ claim ITU-T ở `ONE_PAGE_SUMMARY.md` và `STANDARDS/standards.csv` + `.json` ( AIP → ANP). | Không còn cổng chặn. `docs/PRESS_KIT.md` mục 6.2 nêu rõ điều chúng tôi **không** khẳng định |
| **C8** | Kiểm tra **thủ công** — phải mở hộp thư `nan_ai2ai@proton.me` và xác nhận nhận được | Người phụ trách kiểm tra mở hộp thư |
| **F4** | Chưa đăng bài giới thiệu nào (cần chọn kênh) | Chọn kênh + đăng, ghi lại URL vào `audit.log` |
| **F6** | Chưa khởi tạo nhật ký báo cáo tuần | Tạo file nhật ký tuần trong `C:\NAN_DATA\07_AUDIT\` |

### Những mục đã kiểm chứng và cách kiểm chứng

- **A1–A10**: chạy `python -m unittest discover -s tests -v` (10/10 OK) · chạy demo (exit 0) · `python scripts/license_gate.py` (PASS, 0 blocked) · `py_compile` trên 5 file `.py` (0 lỗi) · parse 2 workflow YAML (0 lỗi) · badge **ci.yml** và **license.yml** đều PASSING (ci.yml: gate + TruffleHog + unit test trên matrix Python 3.8/3.10/3.12; license.yml: gate + `license_gate.py` + ScanCode) · `git status --porcelain` rỗng · `git ls-files` không chứa `LEADS.md`, `_tools/`, `FINAL_CHECK.md`
- **B1**: badge README `White Paper: v0.4-draft` khớp dòng `Phiên bản:` trong file · **B3**: 5/5 điểm minh bạch có trong README · **B4**: Chương 6 có đúng **12** câu hỏi, README không tuyên bố con số khác · **B5**: không có tuyên bố số file nào trong tài liệu · **B7**: 48 file công khai, 0 placeholder thật (4 chuỗi khớp nằm trong chính dòng định nghĩa của mục B7)
- **C1–C7, C9**: HTTP 200 cho repo / whitepaper / issues / releases / web hub / Zalo / Telegram / X / LinkedIn; **100 link tương đối** trong `.md`/`.html` đều tồn tại
- **D1–D7**: LICENSE có đủ "TERMS AND CONDITIONS" + "END OF TERMS" · CLA.md · TRADEMARK.md · HANDOVER.md (12 tháng) · THIRD_PARTY_NOTICES.md 2.352 B, không có `.bak` · SECURITY.md (kênh Email ưu tiên + tab Issues) · CODE_OF_CONDUCT.md
- **E1–E6**: 3 mẫu Issue + mẫu PR trong `.github/` · `config.yml` tắt issue trống + có contact links · **3/3 issue đã gắn `good first issue`** (đã sửa trong đợt kiểm toán này) · CODEOWNERS không còn placeholder
- **F1–F3, F5**: CHANGELOG có mục 0.1.0 · tag `v0.1.0` có trên remote (`refs/tags/v0.1.0` → `c67a714`, đã `git fetch --tags` về local) · GitHub Release "NAN AI2AI - Initial Public Release v0.1.0" không phải draft · `audit.log` đã ghi các mốc

> **Phần ký còn để trống có chủ đích.** Người phê duyệt phát hành ký sau khi 5 mục còn lại được đóng.
