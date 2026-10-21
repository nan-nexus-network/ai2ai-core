# 06 — Checklist Phát Hành (Release Checklist)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026 · Dùng cho **mỗi** lần phát hành

> Nguyên tắc: **cổng nào chưa đạt thì không đi tiếp.** Không "làm tạm". Nếu không kịp hạn, hãy lùi ngày.
> Chi tiết về các cổng G1–G4: [01_LAUNCH_PLAN.md](01_LAUNCH_PLAN.md) mục 2.

---

## Giai đoạn A — Kiểm tra kỹ thuật (tự động)

| # | Kiểm tra | Lệnh | Kỳ vọng | ✅ |
| :---: | :--- | :--- | :--- | :--- |
| A1 | Unit test | `python -m unittest discover -s tests -v` | 6/6 PASS | ☐ |
| A2 | Demo | `python examples/01-hello-agent/hello_bridge.py` | exit 0 | ☐ |
| A3 | Cổng license | `python scripts/license_gate.py` | exit 0, 0 blocked | ☐ |
| A4 | Cú pháp | `python -m py_compile <mọi file .py>` | không lỗi | ☐ |
| A5 | YAML | parse `.github/workflows/*.yml` | OK | ☐ |
| A6 | Tương thích 3.8 | CI matrix | 3/3 xanh | ☐ |
| A7 | Rò rỉ secret | TruffleHog trong CI | 0 phát hiện | ☐ |
| A8 | SPDX header | `python scripts/license_gate.py` | 0 file thiếu | ☐ |
| A9 | Working tree | `git status --porcelain` | rỗng | ☐ |
| A10 | Không còn file gitignored bị commit | `git ls-files` | không có `LEADS.md`, `_tools/`, `FINAL_CHECK.md` | ☐ |

## Giai đoạn B — Nội dung & tính nhất quán

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| B1 | Phiên bản whitepaper trong README **khớp** với dòng `Phiên bản:` trong chính file | ☐ |
| B2 | Mọi trích dẫn pháp lý trong danh mục tham khảo có ngày/số hiệu **đã được đối chiếu** | ☐ |
| B3 | Tuyên bố minh bạch có **đủ 5 điểm** (bản chất, người khởi xướng, 3 cam kết, không đại diện, kỹ thuật giới hạn) trong README | ☐ |
| B4 | Số câu hỏi mở nói trong README **khớp** số câu hỏi trong Chương 6 | ☐ |
| B5 | Số file/tệp nói trong tài liệu **khớp** thực tế | ☐ |
| B6 | `ROADMAP.md` và `CHANGELOG.md` đã cập nhật cho phiên bản này | ☐ |
| B7 | Không còn placeholder (`PLACEHOLDER`, `#thay-link`, `TODO`, `FIXME`) trong tệp **công khai** | ☐ |
| B8 | Không còn tuyên bố về số liệu chưa kiểm chứng | ☐ |

## Giai đoạn C — Liên kết ngoài (thủ công — bắt buộc mở từng link)

| # | Kiểm tra | Kỳ vọng | ✅ |
| :---: | :--- | :--- | :--- |
| C1 | `https://github.com/nan-nexus-network/ai2ai-core` | **200**, không 404 | ☐ |
| C2 | `https://github.com/nan-nexus-network/ai2ai-core/blob/main/docs/WHITEPAPER_VN_AI_BRIDGE.md` | 200 | ☐ |
| C3 | `https://github.com/nan-nexus-network/ai2ai-core/issues` | 200 | ☐ |
| C4 | `https://github.com/nan-nexus-network/ai2ai-core/releases` | 200 | ☐ |
| C5 | `https://nan-ai2ai.pages.dev` | DNS phân giải, 200 | ☐ |
| C6 | Link nhóm Zalo (đã thay `PLACEHOLDER_ZALO`) | vào được nhóm thật | ☐ |
| C7 | Link X.com (`AI2AI_Economy`) | tồn tại — **hoặc đã gỡ nút** | ☐ |
| C8 | Hộp thư `nan.ai2ai.initiative@proton.me` | **nhận được** email | ☐ |
| C9 | Mọi link tương đối trong `.md` / `.html` | file đích tồn tại | ☐ |

> **C1–C8 là điều kiện bắt buộc.** Một link chết ở trang đích tệ hơn nhiều so với việc trễ thêm một ngày.

## Giai đoạn D — Pháp lý & giấy phép

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| D1 | `LICENSE` là Apache 2.0 đầy đủ (9 điều khoản) | ☐ |
| D2 | `CLA.md` có đủ 4 điều khoản | ☐ |
| D3 | `TRADEMARK.md` bảo lưu đủ 3 tên | ☐ |
| D4 | `HANDOVER.md` có cam kết 12 tháng + không rút lại | ☐ |
| D5 | `THIRD_PARTY_NOTICES.md` còn nguyên, **không** bị `make license-report` ghi đè | ☐ |
| D6 | `SECURITY.md` có kênh báo cáo và địa chỉ | ☐ |
| D7 | `CODE_OF_CONDUCT.md` có cơ chế báo cáo | ☐ |

## Giai đoạn E — Cộng đồng

| # | Kiểm tra | ✅ |
| :---: | :--- | :�� |
| E1 | 3 mẫu Issue hiển thị đúng trong tab Issues (`.github/ISSUE_TEMPLATE/`) | ☐ |
| E2 | Mẫu Pull Request hiển thị khi mở PR | ☐ |
| E3 | `config.yml` — Issue trống đã tắt, có contact links | ☐ |
| E4 | Có ít nhất **3** đầu việc gắn `good first issue`, mỗi cái đủ cụ thể | ☐ |
| E5 | `CODEOWNERS` đã thay placeholder bằng tên GitHub thật | ☐ |
| E6 | `CODE_OF_CONDUCT.md` không chứa placeholder | ☐ |

## Giai đoạn F — Phát hành

| # | Việc | ✅ |
| :---: | :--- | :�� |
| F1 | `CHANGELOG.md` có mục cho phiên bản này | ☐ |
| F2 | Tag + push: `git tag -a v0.1.0 -m "..." && git push origin v0.1.0` | ☐ |
| F3 | Tạo GitHub Release kèm tóm tắt 1 trang | ☐ |
| F4 | Đăng 1 bài giới thiệu (kênh nào đã sẵn sàng) | ☐ |
| F5 | Ghi lại thời điểm phát hành vào `audit.log` | ☐ |
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
