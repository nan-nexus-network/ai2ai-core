# Nhật Ký Phát Hành (Changelog)

Dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/). Mọi mục ghi theo thời gian UTC.

> **Lưu ý phiên bản:** Mã nguồn hiện ở `v0.1` (PoC). Tài liệu thảo luận được đánh phiên bản **riêng**
> (`v0.4-draft`) vì nó đi trước mã nguồn — đây là chủ ý: tài liệu là đề xuất để phản biện, mã nguồn là thứ
> đã chạy được và được kiểm thử.

---

## [Chưa phát hành] — v0.2.0-dev (đang phát triển)

### Bổ sung

- **Atomic In-flight Claim** — chống thực thi lặp **đồng thời** (race condition → double-spend). Khoá `threading.Lock` bảo vệ mọi biến đổi trạng thái; mỗi `operation_id` đang xử lý có một `threading.Event` để request thứ hai **chờ** thay vì chạy lại. Cơ chế nằm trong `nan_ai2ai/idempotency.py` và dùng **chỉ thư viện chuẩn Python**.
- `ProtocolBridgeNode.execute_with_idempotency()` — claim khoá **trước khi** gọi bên thực thi. Đây là điểm khác biệt cốt lõi: chỉ khoá ở bước cấp biên nhận thì tác vụ **đã** chạy hai lần.
- `docs/ADR_003_ATOMIC_IN_FLIGHT_CLAIM.md` — ghi lại quyết định, gồm cả lý do **không tự chạy lại** khi lần chạy trước lỗi (tác vụ có thể đã có tác dụng phụ).

### Sửa

- `hello_bridge.py` và `agent_chat.py` dùng chung bộ máy idempotency (mỗi bridge một kho riêng) để logic khoá **không trôi khỏi nhau** giữa hai hiện thực.
- `agent_chat.py`: Agent B giờ được gọi **bên trong** claim, nên retry đồng thời cũng chỉ thực thi một lần.

### Bổ sung

- **Gói `nan_ai2ai/`** — mã nguồn tham chiếu có thể import được (gói ở thư mục gốc, không cần bước cài đặt).
- **`nan_ai2ai/validation.py`** — bộ kiểm tra cấu trúc bằng **thư viện chuẩn Python**: allowlist trường, kiểu dữ liệu, độ dài, miền giá trị. Là **subset** của JSON Schema Draft 2020-12, không phải bản triển khai đầy đủ.
- **`nan_ai2ai/ed25519.py`** — Ed25519 thuần Python theo **RFC 8032**, giữ cam kết "Zero Dependencies". Kiểm chứng bằng 5 vector chính thức RFC 8032 §7.1 và đối chiếu chéo với `cryptography` (25/25 mẫu ngẫu nhiên).
- **`nan_ai2ai/canonical.py`** — chuẩn hoá JSON + băm có **domain separator** và **length prefix**, thay cho cách nối trực tiếp hai chuỗi JSON ở v0.1.
- **`nan_ai2ai/receipt.py`** — biên nhận `nan-receipt/v1`: **chỉ bên thực thi ký**, `nonce` + `expires_at` chống replay, `kid` = JWK thumbprint RFC 7638.
- **`nan_ai2ai/trust.py`** — mô hình neo tin cậy **TOFU** + Agent Card tối giản tương thích hình dạng A2A.
- **`examples/03-signed-receipt/signed_receipt_demo.py`** — ví dụ chứng minh bên thứ ba xác minh biên nhận **mà không cần tin Bridge**.
- **`docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`** — ghi lại 4 quyết định kiến trúc.
- Bộ test: **10 → 100 test** (`tests/test_ed25519.py`, `test_validation.py`, `test_canonical.py`, `test_receipt.py`).

### Sửa

- `docs/ADR_001.md` — mục L3 và L5 được cập nhật; **giải quyết mâu thuẫn** giữa yêu cầu "JSON Schema Draft 2020-12" (L37) và "chỉ dùng thư viện chuẩn" (Issue #1 L19) bằng cách nêu rõ đây là *subset*.
- `ROADMAP.md` — mục v0.2 cập nhật trạng thái thực tế; thêm mục **Backlog dài hạn** (GB/Z adapter, transparency log, backend `cryptography`, hợp nhất 2 bridge, đóng gói chuẩn).

### Ghi chú trước khi phát hành

### Bổ sung
- Khung pháp lý đầy đủ: `LICENSE` (Apache 2.0), `CLA.md`, `TRADEMARK.md`, `HANDOVER.md`, `THIRD_PARTY_NOTICES.md`
- PoC mẫu 60 giây (`examples/01-hello-agent/hello_bridge.py`) — 100% thư viện chuẩn Python, 0 dependency
- 10 unit test cho luồng dịch MCP → A2A, biên nhận SHA-256, chống prompt injection và kiểm tra JSON đầu vào
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
