# TECHNICAL DEBT - NAN AI2AI-SI2SI

> **Đây là danh sách các tồn đọng kỹ thuật cần đội ngũ Core Contributor tương lai xử lý. Không sửa vào lúc này để bảo toàn nguồn lực cho chiến dịch truyền thông.**
>
> Tài liệu này được mở ngày **22/10/2026** nhằm chuyển trọng tâm công việc sang chiến dịch truyền thông định hướng (Nền kinh tế AI · A2A/AI2AI · Cơ chế bằng chứng kỹ thuật trung lập).

**Trạng thái repo tại thời điểm lập file:** `ai2ai-core` HEAD `71c780a` · 29 commit · 121 unit test PASS · CI 11/11 job SUCCESS · working tree CLEAN.
**Kho tài liệu:** `ai2ai-research` HEAD `41e9dc1` · `data-check.yml` SUCCESS.

---

## 0. ĐỌC TRƯỚC KHI NHẬN VIỆC

Tài liệu này chia làm **hai phần**, và điều đó quan trọng:

| Phần | Nội dung | Trạng thái |
|:--|:---|:---|
| **A** | 17 lỗi phát hiện trong đợt rà soát dòng-by-dòng ngày 22/10 | **ĐÃ SỬA** - giữ lại làm hồ sơ và để giải thích vì sao các kiểm tra tự động tồn tại |
| **B** | Nợ kỹ thuật **thực sự còn mở** | **CẦN LÀM** - đây mới là danh sách việc cho Core Contributor tương lai |

> ⚠️ **Lưu ý về Phần A.** Nhóm công việc trước đã sửa **toàn bộ 17 lỗi** và đẩy lên GitHub (xem mục A.2) **trước khi tài liệu này được mở**. Vì vậy Phần A được ghi lại ở đây **không phải** để báo rằng các lỗi đó còn tồn tại trong mã, mà để:
> 1. lưu hồ sơ **có kiểm chứng** (lỗi gì, ở đâu, sửa bằng cách nào, ở commit nào);
> 2. chỉ ra **cơ chế nào đã được thêm để lỗi đó không tái diễn**;
> 3. giải thích cho người đọc tại sao các kiểm tra trong CI có vẻ "không liên quan gì", nhưng chúng có liên quan.
>
> **Phần B mới là việc thật sự còn treo.**

---

# PHẦN A - 17 LỖI ĐỢT RÀ SOÁT 22/10 · TRẠNG THÁI: ĐÃ SỬA

## A.1. Tóm tắt

| Nhóm | Số lỗi | Nội dung |
|:---|--:|:---|
| Chính tả | 12 | `Kết luốn`→`Kết luận` · `dẫn dẫn`→`dẫn dắt` · `Đã đối chiểu`→`Đã đối chiếu` · `nghiin`→`nghin` · `Doi pha`→`Dot pha` · `thu manh`→`the manh` · `thu vien so`→`cong nghe thong tin, kinh te so` · `Tien deu`→`Tien de` · `khuc-vuc`→`khu-vuc` · `cong-boc`→`cong-bo` · `luat vuc`→`khu vuc` · chữ Hán `谦`→`谅` |
| Câu lặp | 1 | Câu *"NAN AI2AI cung cấp một sân chơi thực hành mở…"* lặp 2 lần liên tiếp trong whitepaper |
| Mâu thuẫn nhà xuất bản | 1 | Báo cáo *Economic Impact Report* của Google do **Access Partnership** thực hiện, **không phải NIC**, mâu thuẫn với bảng xác minh |
| Dịch sai cơ quan ban hành | 1 | `Viện Hàn lâm Viễn thông` → **Cục Quản lý Không gian mạng Quốc gia (CAC)** (đúng với `国家互联网信息办公室`) |
| Thuật ngữ GB/Z không thống nhất | 1 | "bộ tiêu chuẩn quốc gia" → **"bộ văn bản kỹ thuật chỉ dẫn chuẩn hoá quốc gia"** (6 chỗ) |
| Đồng bộ CSV ↔ JSON | 1 | 5 dòng lệch ở trường `issuer`/`scope`/`name_local` (kể cả chữ Hán sai trong JSON) |

**Ngoài ra, phát hiện thêm 1 lỗi trong lúc kiểm chứng:** `ONE_PAGE_SUMMARY.md` và `ABSTRACT_EN.md` còn viết *"chữ ký Ed25519 chưa có"*, đã lỗi thời vì `v0.2` đã có biên nhận `nan-receipt/v1` ký bởi bên thực thi. Đã cập nhật, kèm giữ nguyên các hạn chế còn lại.

## A.2. Commit đã sửa

| Kho | Commit | Nội dung |
|:--|:--|:---|
| `ai2ai-research` | `9187ba7` | 17 lỗi (văn xu + dữ liệu) + cập nhật claim chữ ký + ghi chú 17+6=23 + sửa "How to Cite" |
| `ai2ai-research` | `41e9dc1` | 2 lỗi dữ liệu cuối (`Tien deu`, mô tả trường `jurisdiction`) |
| `ai2ai-core` | `71c780a` | Bản whitepaper chuẩn, **giữ byte-for-byte giống** bản trong kho research |

## A.3. Cơ chế đã thêm để lỗi không tái diễn

Đây là phần **quan trọng nhất** của Phần A: mỗi lớp bảo vệ gắn với một loại lỗi:

| Loại lỗi | Cơ chế bảo vệ | Ở đâu |
|:---|:---|:---|
| `source_ref` trỏ sai số tham khảo | Validator **đọc whitepaper**, đối chiếu từng `Tham khao N` với mục N thật (số **và** nội dung có chứa văn bản đó) | `ai2ai-research/scripts/validate_dataset.py` mục [3] |
| Số văn bản lệch giữa các ngôn ngữ | Validator quét mọi câu "N văn bản" trong `README.md` / `CHANGELOG.md` / `CITATION.cff` và đòi N = số dòng thật | cùng file, mục [4] |
| CSV lệch JSON | Validator đối chiếu id, thứ tự, và (sau đợt này) **mọi trường** | cùng file, mục [2] |
| Claim lỗi thời về tính năng | Rà soát dòng-by-dòng có so sánh với **mã nguồn thật**; claim chữ ký đã cập nhật theo `v0.2` | rà soát 22/10 |
| 2 bản whitepaper lệch nhau | Kiểm tra byte-for-byte giữa `ai2ai-core/docs/` và `ai2ai-research/PAPERS/` | quy trình kiểm toán |
| Dấu vết Gitee còn sót | `verify_china_kit.ps1` kiểm **không còn tham chiếu Gitee** + **có link GitHub** trong bài sẽ đăng | `_git_tools/` |

> **Ghi chú kỹ thuật:** chính cơ chế [4] (đếm số văn bản) **báo động giả** khi mới viết, vì nó đọc "6 văn bản" và "7 văn bản" trong `CHANGELOG` là số **tập con** (6 mục dẫn chiếu trong thân bài; 7 phần GB/Z), không phải tổng số văn bản của dataset. Đã sửa để phân biệt theo **ngữ cảnh phía sau số**.

---

# PHẦN B - NỢ KỸ THUẬT THỰC SỰ CÒN MỞ

> **Đây là danh sách các tồn đọng kỹ thuật cần đội ngũ Core Contributor tương lai xử lý. Không sửa vào lúc này để bảo toàn nguồn lực cho chiến dịch truyền thông.**
> Ưu tiên **P1** = cản trở tính đáng tin cậy · **P2** = mở rộng năng lực · **P3** = vệ sinh kỹ thuật.

## B.1. Bảo mật & niềm tin (P1)

| # | Vấn đề | Vì sao còn mở | Việc cần làm |
|:--|:---|:---|:---|
| B1.1 | **Neo tin cậy chỉ là TOFU** | `nan_ai2ai/trust.py` ghim khoá công khai **lần đầu nhìn thấy**. Đây là mô hình TOFU thuần, bảo vệ được từ lần tiếp xúc thứ hai trở đi, **không** bảo vệ được lần đầu (MITM trước khi ghim) | Chọn và tài liệu hoá mô hình neo: TOFU + khoá ngoài tuyến, **hoặc** DID (đã cân nhắc ở ADR-002, xem lại quyết định), **hoặc** transparency log |
| B1.2 | **Chưa có transparency log** | Muốn tuyên bố biên nhận "kiểm chứng độc lập" thì cần log append-only công khai | Backlog **BL2** |
| B1.3 | **Ed25519 thuần Python không constant-time** | `nan_ai2ai/ed25519.py` viết tay để giữ cam kết "Zero Dependencies". Chỉ dùng cho **dữ liệu công khai** nên chấp nhận được, nhưng cần nói rõ giới hạn ở mọi nơi | Backlog **BL3**: backend `cryptography`/HSM, giữ bản thuần làm tham chiếu |
| B1.4 | **Chưa có chống replay xuyên tiến trình** | Dedup cache nằm trong bộ nhớ **một tiến trình**. Mất khi restart; không dùng chung giữa các nút | Cần khoá phân tán (Redis, v.v.), thuộc phạm vi hạ tầng, chưa phải PoC |
| B1.5 | **Chưa có log audit cho mỗi lần claim idempotency** | Không truy vết được ai giữ khoá lúc nào | Bổ sung vào `nan_ai2ai/idempotency.py` (đã có chỗ để móc) |
| B1.6 | **Blocklist tĩnh vẫn là lớp phòng thủ thứ hai** | `hello_bridge.py` L2 vẫn quét 5 chuỗi tĩnh; tự thừa nhận gây false-positive (ví dụ ghi chú hàng hoá *"drop table shipment at port"*) | Semantic Classifier + Allowlist Schema (đã ghi trong `hello_bridge.py` và `Issue #1`) |
| B1.7 | **Chưa có transport, xác thực, phân quyền** | PoC chạy cục bộ, một tiến trình, dữ liệu mô phỏng | Nằm ngoài phạm vi PoC, nêu rõ trong mọi tài liệu |

## B.2. Kiến trúc & dữ liệu (P1–P2)

| # | Vấn đề | Việc cần làm |
|:--|:---|:---|
| B2.1 | **Hai hiện thực bridge vẫn tách rời**: `examples/01-hello-agent/hello_bridge.py` (`ProtocolBridgeNode`) và `examples/02-agent-to-agent-chat/agent_chat.py` (`NANBridgeNode`): khác class, khác schema biên nhận, **khác cả kho dedup**. Logic khoá đã tách ra `nan_ai2ai/idempotency.py` để không trôi, nhưng **giao diện** vẫn chưa thống nhất | Backlog **BL4**: hợp nhất thành một interface. *Đây là nợ kỹ thuật được ghi nhận rõ nhất trong toàn bộ lịch sử dự án.* |
| B2.2 | **Chưa có đóng gói chuẩn**: gói `nan_ai2ai/` nằm ở thư mục gốc, không có `pyproject.toml`, không cài được bằng `pip install` | Backlog **BL5** |
| B2.3 | **Validator là subset Draft 2020-12**, chưa hỗ trợ `$ref`, `if/then/else`, `unevaluatedProperties`, `contains`, `dependentSchemas`… Từ khoá ngoài subset **gây lỗi tường minh** (đúng thiết kế) | Mở rộng subset, hoặc chấp nhận giới hạn và ghi rõ trong tài liệu API |
| B2.4 | **Chưa có adapter GB/Z 185** | Backlog **BL1**: điều kiện: có **toàn văn** chuẩn **và** bộ test vector tương thích. Hiện repo **không** có nội dung quy chuẩn |
| B2.5 | **Chưa có CI kiểm tra 2 bản whitepaper đồng bộ byte** | Hiện kiểm thủ công bằng `git show` + so sánh. Nên đưa vào CI |
| B2.6 | **`ai2ai-research` chưa có Release / bản PDF** | `PRESS_KIT.md` hứa tải PDF từ GitHub Releases, hiện **chưa có** PDF nào được đính kèm. Cần tạo hoặc sửa lời hứa |

## B.3. Vận hành & phát hành (P2–P3)

| # | Vấn đề | Việc cần làm |
|:--|:---|:---|
| B3.1 | ~~**Repo rỗng còn sót** ở tài khoản cá nhân: `nexusasianetwork-NAN/ai2ai-research` (0 KB)~~ | ✅ **ĐÃ XOÁ 22/10/2026** bởi Chủ tịch (Settings → Danger Zone). API xác nhận HTTP 404 cho cả `ai2ai-research` lẫn `ai2ai-core` ở tài khoản cá nhân. Rủi ro "hai nguồn chính thức" đã dẹp. Kho thật trong org `nan-nexus-network` nguyên vẹn |
| B3.2 | **Chưa có Discussion nào** dù Discussions đã bật cả 2 kho | Bài "Tại sao lại là Việt Nam?" đã soạn sẵn (`07_DISCUSSION_DRAFT_VN.md`) |
| B3.3 | **Chưa có quy trình trả lời Issue** ghi thành văn bản | Đã có cam kết 48 giờ trong `CONTRIBUTING.md`; cần mẫu trả lời cho người đóng góp lần đầu (đã có 1 trường hợp thật: `dharsinir15-priya`) |
| B3.4 | **Bộ Não & Skill (3.131 file) chưa có chiến lược công bố** | Tài sản trí tuệ lớn nhất, cũng là rủi ro lớn nhất nếu tài liệu truyền thông dẫn tới đường dẫn cục bộ. Xem `ASSET_INVENTORY_20261022.md` mục 2.4 |
| B3.5 | **Chưa có log kiểm toán tập trung** cho các kho tài liệu (`ai2ai-research`, kho tài liệu truyền thông) | `ai2ai-core` đã có `audit.log`; các kho còn lại chưa |
| B3.6 | **4 câu "GB/Z → ITU-T" đã gỡ** nhưng **chưa có nguồn xác minh thay thế** | Nếu sau này muốn khẳng định về tiến độ quốc tế hóa, cần số hiệu văn bản ITU-T cụ thể. Hiện trạng đã trung thực: nói rõ **không xác minh được** |

---

## C. GHI CHÚ CHO NGƯỜI NHẬN VIỆC

1. **Đọc `docs/ADR_001.md` trước.** Dự án tự định vị là **Open Reference Framework**, **không phải** Protocol. Đừng đề xuất thêm một giao thức mới.
2. **Đọc `docs/ADR_002.md`** (biên nhận có chữ ký, mô hình neo tin cậy) và **`docs/ADR_003.md`** (claim nguyên tử chống thực thi lặp đồng thời) trước khi đụng vào `nan_ai2ai/`.
3. **Các bài kiểm tra trong CI không phải ngẫu nhiên.** Chúng sinh ra từ 17 lỗi thật ở Phần A. Đừng xoá hay nới lỏng chúng.
4. **Giữ "Zero Dependencies"** ở `nan_ai2ai/` trừ khi thực sự cần (xem B1.3 và B2.2).
5. **Nếu sửa whitepaper, sửa cả hai bản** (`ai2ai-core/docs/` và `ai2ai-research/PAPERS/`) và kiểm tra byte-for-byte.
6. **Mọi khẳng định về tính năng phải khớp mã nguồn thật.** Đợt rà soát 22/10 bắt được một claim *"chữ ký Ed25519 chưa có"* đã lỗi thời, vì `v0.2` đã có.
7. **Ghi mọi thay đổi vào `audit.log`** và commit với thông điệp nói rõ **điều gì đã sai** và **vì sao sửa**, không chỉ nói *đã sửa*.

---

*Bản này thay thế mọi tuyên bố "còn 17 lỗi chưa sửa". 17 lỗi đó **đã** được sửa và push (Phần A.2). Việc còn mở nằm ở Phần B.*
