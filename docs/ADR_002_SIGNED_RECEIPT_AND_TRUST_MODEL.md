# ADR-002: Biên nhận có chữ ký, mô hình neo tin cậy, và bộ kiểm tra cấu trúc

**Ngày:** 21/10/2026 · **Trạng thái:** Đã chấp nhận (Accepted) · **Thay thế:** không
**Liên quan:** `docs/ADR_001.md` (định vị dự án), `.github/ISSUE_TEMPLATE/ISSUE_1_SECURITY_BLOCKLIST.md`, `ISSUE_2_CRYPTOGRAPHY_ED25519.md`

---

## 0. Bối cảnh

`v0.1` đã công bố một PoC minh hoạ ý tưởng "cầu nối giao thức". Kiểm toán kỹ thuật (21/10/2026) đo được các hạn chế cụ thể bằng cách chạy mã:

| Hạn chế | Kết quả đo |
|:---|:---|
| Blocklist tĩnh chỉ kiểm tra **sự tồn tại** của trường | `route=""`, `route=12345`, `cargo_type=None`, `route` dài 10.000 ký tự, `arguments` có 500 khoá → **5/5 vẫn "hợp lệ"** |
| `max_latency_hours` không được kiểm tra kiểu dữ liệu | giá trị chuỗi `"KHONG_PHAI_SO_AM_TIEN"` đi thẳng vào `standardized_task.parameters` |
| Biên nhận không có chữ ký | đổi thẳng trường `sha256_proof` → **không có gì chặn** |
| Băm bằng cách nối hai blob JSON | `json.dumps(a) + json.dumps(b)` — **không dấu phân cách, không domain separator** |
| Hai hiện thực bridge phân kỳ | `hello_bridge.py` (`ProtocolBridgeNode`, `NAN-AI2AI-Bridge/v0.1-poc`, `DEMO_DIGEST_ONLY`, **có** gọi validation) vs `agent_chat.py` (`NANBridgeNode`, `NAN-AI2AI/v1.0`, `DIGEST_ISSUED_BY_NAN_BRIDGE`, **không** gọi validation) |

Đồng thời, ba câu hỏi còn treo:

1. `ADR_001.md` L37 yêu cầu "JSON Schema Draft 2020-12" ↔ `Issue #1` L19 yêu cầu "chỉ dùng thư viện chuẩn của Python".
2. Phạm vi ký biên nhận: chỉ executor, hay executor + bridge?
3. Mô hình neo tin cậy: registry tập trung / DID / TOFU + transparency log?
4. GB/Z adapter: giữ trong backlog dài hạn hay gỡ khỏi v0.2?

---

## 1. Quyết định 1 — Bộ kiểm tra cấu trúc: **subset Draft 2020-12 bằng stdlib, và sửa lại ADR-001**

**Chọn:** *Cả hai* — không phải "một trong hai".

**Lý do:**

- `jsonschema` (PyPI) sẽ **phá cam kết "Zero Dependencies"** đang treo ở tiêu đề README (mục "Chạy Thử Nghiệm Trong 60 Giây"). Đây là claim đã công bố công khai, không thể âm thầm bỏ.
- JSON Schema **Draft 2020-12 đầy đủ** dùng các từ khoá `$ref`, `$dynamicRef`, `if/then/else`, `unevaluatedProperties`, `contains`, `dependentSchemas`… — không thể viết lại đầy đủ bằng stdlib trong phạm vi hợp lý.
- Nhưng vấn đề cần giải **không phải** "có tương thích Draft 2020-12 hay không" — đó là **kiểm tra được kiểu dữ liệu, độ dài, miền giá trị, và chỉ cho phép đúng những trường được phép**. Đó là subset, và subset làm được bằng stdlib.

**Cách thực hiện:**

- `nan_ai2ai/validation.py` cài đặt subset gồm: `type`, `required`, `properties`, `additionalProperties`, `enum`, `const`, `minimum`/`maximum`/`exclusiveMinimum`/`exclusiveMaximum`, `minLength`/`maxLength`, `minItems`/`maxItems`, `pattern`, `items`, `propertyNames`, `multipleOf`.
- **Từ khoá ngoài subset sẽ gây lỗi tường minh**, không bị bỏ qua âm thầm. Nếu bỏ qua, một schema "trông hợp lệ" có thể thực ra không kiểm tra gì — trạng thái nguy hiểm hơn cả việc không có validator.
- `ADR_001.md` L37 được sửa để nói rõ: *"JSON Schema (Draft 2020-12 **subset**), tự triển khai bằng thư viện chuẩn Python; **không phải** bản triển khai đầy đủ của Draft 2020-12"*.

**Kiểm chứng:** `tests/test_validation.py` — 32 test, gồm đúng 5 lỗ hổng đo được ở v0.1, nay đều bị chặn.

---

## 2. Quyết định 2 — Phạm vi ký: **chỉ executor**; Bridge chỉ được "ghi nhận"

**Chọn:** `signatures` chỉ chứa chữ ký của **executor**. Bridge không được ký trong trường này.

**Lý do — đây là mấu chốt của toàn bộ thiết kế:**

Nếu Bridge ký, bên thứ ba buộc phải quyết định "có tin Bridge không". Nếu chỉ executor ký thì:

- Bridge **không thể** làm giả biên nhận (không có khoá executor).
- Bridge **không thể** sửa kết quả (`result_digest` nằm trong phạm vi chữ ký của executor).
- Bên thứ ba xác minh được **mà không cần tin bất kỳ bên trung gian nào**.

Đó chính xác là câu hỏi đã nêu ở vòng đánh giá trước: *"làm sao để biên nhận kiểm chứng được bởi bên thứ ba mà không cần tin vào Bridge?"*. Ký bằng khoá Bridge **không giải quyết** câu hỏi đó — nó chỉ làm biên nhận "trông đáng tin hơn mà chứng minh ít hơn".

**Còn "Bridge đã thấy gì" thì đặt ở đâu?** Ở trường riêng `transporter_attestations`, với mỗi mục mang trường `evidentiary_weight: "none"`. Trường này **không bao giờ** được dùng để quyết định "biên nhận có hợp lệ hay không". Nó phục vụ trao đổi nội bộ giữa các node.

**Kiểm chứng:** `tests/test_receipt.py::TestSigningScope` — `sign_receipt(..., role="bridge")` ném lỗi; `test_transporter_attestation_does_not_affect_verification` chứng minh thêm bằng chứng của Bridge không đổi kết quả xác minh.

---

## 3. Quyết định 3 — Mô hình neo tin cậy: **TOFU + Agent Card tương thích A2A, log minh bạch để v0.3+**

**Chọn:** phương án **C** (TOFU), với định dạng phân phối khoá lấy từ A2A.

| Phương án | Đánh giá |
|:---|:---|
| **A. Registry tập trung** | ❌ **Bác.** ROADMAP (mục "Những gì dự án **không** làm") ghi rõ: *"Không cung cấp dịch vụ, API hay hạ tầng chạy thật"*. Dự án một người, ~10 giờ/tuần — không có nguồn lực vận hành. Trái ADR-001. |
| **B. DID** | 🟡 **Để ngỏ, không phụ thuộc.** Công thức thực thi được (ANP dùng DID-WBA + WebVH), nhưng đòi hỏi hạ tầng resolver và vòng đời tin cậy (DID document). Vuợt xa năng lực hiện tại, và **không cần thiết** để chứng minh một biên nhận. |
| **C. TOFU + Agent Card** | ✅ **Chọn.** Không cần hạ tầng, không cần chạy dịch vụ, dùng được ngay. |

**Cụ thể:**

- `kid` = **JWK thumbprint (RFC 7638)** — định danh khoá không cần registry.
- Agent Card là **kênh phân phối khoá công khai**. Dự án **không** phát minh lại Agent Card: `nan_ai2ai/trust.py::agent_card` tạo một card tối giản dùng **đúng tên trường** của A2A (`name`, `version`, `provider`, `capabilities`, `skills`, `supportedInterfaces`, `signatures`, `securityRequirements`) để có thể gắn trực tiếp.
  - Căn cứ: `specification/a2a.proto` của `a2aproject/A2A` khai báo `AgentCard.signatures` là *"JSON Web Signatures computed for this AgentCard"* (JWS theo RFC 7515) và `security_requirements` theo từng skill.
  - Card do NAN tạo **không phải** bản Agent Card chính thức của A2A, và được nói rõ như vậy ngay trong docstring.
- **DID không bị loại tranh**: nếu một agent có DID, trường `did` có thể mang trong card. Định dạng biên nhận **không phụ thuộc DID**.
- **Transparency log (Sigstore/Rekor-style)**: để **v0.3+**. Cần để tuyên bố "kiểm chứng độc lập"; v0.2 không tuyên bố điều đó.

**Hạn chế phải nói thẳng (không giấu):** TOFU bảo vệ được từ lần tiếp xúc thứ hai trở đi, **không** bảo vệ được lần tiếp xúc đầu tiên. Một kẻ phát động MITM trước khi bên xác minh ghim khoá có thể thay khoá. Với mức độ tin cậy cao, cần thêm khoá công khai ngoài tuyến, hoặc transparency log.

**Kiểm chứng:** `tests/test_receipt.py::TestThirdPartyVerification` — `test_bridge_cannot_forge_a_receipt`, `test_bridge_cannot_alter_result_without_executor_key`, `test_verifier_needs_only_pinned_key`.

---

## 4. Quyết định 4 — GB/Z adapter: **gỡ khỏi v0.2, giữ vào backlog dài hạn**

**Chọn:** gỡ khỏi phạm vi v0.2.

**Lý do:**

- **Toàn văn chuẩn không nằm trong repo.** `STANDARDS/standards.csv` của kho `ai2ai-research` chỉ mang `source_ref` trỏ tới vị trí trích dẫn, **không** mang nội dung quy chuẩn.
- Viết adapter cho một chuẩn mình **không đọc được** thì không kiểm chứng được — vi phạm nguyên tắc "minh bạch trước, cam kết sau" của ROADMAP.
- V0.2 còn phải đảm bảo cam kết bàn giao 12 tháng (`HANDOVER.md`) và mục tiêu "≥3 implementation độc lập" của ADR-001. Dồn năng lực vào một adapter không kiểm chứng được là rủi ro không cần thiết.

**Điều kiện để đưa lại vào phạm vi:** có trong tay toàn văn GB/Z 185-2026 **và** một bộ vector kiểm thử tương thích (test vectors) để chứng minh adapter đúng.

**Luận điểm chiến lược giữ nguyên:** bản trắng còn nói *"Việt Nam không cần phát minh lại bánh xe, chỉ cần làm bridge tương thích đa chuẩn"* — đó là luận điểm **dài hạn**, không phải cam kết kỹ thuật cho v0.2.

---

## 5. Hệ quả thiết kế kèm theo

| # | Hệ quả | Xử lý |
|:--|:---|:---|
| 1 | Ed25519 phải làm thuần Python (không `cryptography`/`PyNaCl` — cả hai là PyPI) | `nan_ai2ai/ed25519.py` triển khai RFC 8032. **Cảnh báo:** không constant-time, chỉ dùng cho dữ liệu công khai. Kiểm chứng bằng **5 vector chính thức RFC 8032 §7.1** + đối chiếu chéo với `cryptography` (25/25 mẫu ngẫu nhiên khớp tuyệt đối cả khoá công khai lẫn chữ ký). |
| 2 | Cần đóng gói để import được | Gói `nan_ai2ai/` ở thư mục gốc (không cần bước cài đặt, `python -m unittest` từ thư mục gốc là chạy được). Việc đóng gói chuẩn (`pyproject.toml`, src layout) để v0.3. |
| 3 | Cần định danh khoá không registry | `kid` = JWK thumbprint RFC 7638. |
| 4 | Cần chống replay | `nonce` (16 byte ngẫu nhiên) + `expires_at`; bên xác minh tự từ chối biên nhận hết hạn. |
| 5 | Cần băm không nhập nhằng | `canonical.digest_input` thêm **domain separator** + **độ dài 4 byte big-endian** trước mỗi phần, lấy cảm hứng từ RFC 6962 (Certificate Transparency) và RFC 8032 §5.1.5. |
| 6 | Hai hiện thực bridge đang phân kỳ | **Chưa** hợp nhất trong v0.2 — cần một quyết định riêng về phạm vi. Hiện đã **công khai** trong `03_CSDN_TUTORIAL_ZH.md` (bài CSDN dạy chạy `agent_chat.py`) rằng đây là hai hiện thực độc lập chưa hợp nhất. |

---

## 6. Những gì quyết định này **không** làm

- Không biến NAN AI2AI thành một protocol mới (giữ nguyên ADR-001: **Open Reference Framework**).
- Không tuyên bố biên nhận có giá trị pháp lý.
- Không tuyên bố validator tương thích đầy đủ JSON Schema Draft 2020-12.
- Không tuyên bố TOFU chống được tấn công MITM ở lần tiếp xúc đầu tiên.
- Không xây registry, không cung cấp dịch vụ, không phát hành token (ROADMAP — "Những gì dự án **không** làm").

---

## 7. Đối chiếu bằng chứng

| Quyết định | Bằng chứng kiểm chứng |
|:--|:---|
| 1 — validator subset | `tests/test_validation.py` (32 test) · 5 lỗ hổng đo được ở v0.1 nay đều bị chặn · từ khoá ngoài subset gây lỗi tường minh |
| 2 — chỉ executor ký | `tests/test_receipt.py::TestSigningScope` (4 test) |
| 3 — TOFU + card A2A | `tests/test_receipt.py::TestTrustStore` (5 test) + `::TestThirdPartyVerification` (4 test) + `::TestAgentCard` (4 test) |
| 4 — gỡ GB/Z khỏi v0.2 | `ROADMAP.md` mục v0.2 không còn mục GB/Z; thêm vào backlog dài hạn kèm điều kiện |
| Ed25519 | `tests/test_ed25519.py` (17 test) · 5 vector RFC 8032 §7.1 · đối chiếu chéo `cryptography` 25/25 |
| Tổng | `python -m unittest discover -s tests -v` → **100 test, OK** (v0.1: 10 test) |
