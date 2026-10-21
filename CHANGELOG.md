# Nhật Ký Phát Hành (Changelog)

Dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/). Mọi mục ghi theo thời gian UTC.

> **Lưu ý phiên bản:** Mã nguồn hiện ở `v0.1` (PoC). Tài liệu thảo luận được đánh phiên bản **riêng**
> (`v0.4-draft`) vì nó đi trước mã nguồn — đây là chủ ý: tài liệu là đề xuất để phản biện, mã nguồn là thứ
> đã chạy được và được kiểm thử.

---

## [Chưa phát hành] — Đang chuẩn bị v0.1.0

### Bổ sung
- Khung pháp lý đầy đủ: `LICENSE` (Apache 2.0), `CLA.md`, `TRADEMARK.md`, `HANDOVER.md`, `THIRD_PARTY_NOTICES.md`
- PoC mẫu 60 giây (`examples/01-hello-agent/hello_bridge.py`) — 100% thư viện chuẩn Python, 0 dependency
- 6 unit test cho luồng dịch MCP → A2A, biên nhận SHA-256, chống prompt injection
- Tài liệu thảo luận mở 7 chương với 12 câu hỏi mở cho cộng đồng
- CI: quét secret (TruffleHog, pin theo SHA) + test trên Python 3.8/3.10/3.12 + cổng kiểm tra license
- Cổng kiểm tra license: `scripts/license_gate.py` + allowlist + `make license-check`
- 3 mẫu Issue trong `.github/ISSUE_TEMPLATE/` (Security, Cryptography, Testing)
- Bộ tài liệu kế hoạch công khai: `docs/public_launch/` (7 tài liệu)
- Quản trị dự án công khai: `GOVERNANCE.md` (kèm quy trình leo thang bất đồng), `SECURITY.md`, `CODE_OF_CONDUCT.md`
- `ROADMAP.md`, `SUPPORT.md`, `.gitattributes`, `.editorconfig`, `CITATION.cff`
- Mẫu Pull Request và cấu hình Issue (`config.yml`)

### Sửa
- Thêm SPDX header `Apache-2.0` cho toàn bộ mã nguồn nội bộ
- `make license-report` không còn ghi đè `THIRD_PARTY_NOTICES.md`
- Chuẩn hóa BOM/CRLF về UTF-8 không BOM + LF

### Ghi chú trước khi phát hành
Còn 3 việc thủ công phía Chủ tịch (tạo tài khoản, liên kết ngoài, điền placeholder) —
xem `docs/public_launch/06_RELEASE_CHECKLIST.md`.

---

## Định dạng

Dự án dùng [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/) và
[Conventional Commits](https://www.conventionalcommits.org/).
