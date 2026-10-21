# 03 — Đo Lường & Báo Cáo (Metrics & Measurement)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026 · **Chu kỳ:** hằng tuần (nhẹ) + hằng tháng (đầy đủ)

---

## 1. Nguyên tắc đo lường

1. **Chỉ đo thứ ta sẽ hành động theo.** Một chỉ số không dẫn tới quyết định nào thì không đo.
2. **Công bố cả chỉ số xấu.** Đặc biệt là những cái đo được và không đạt.
3. **Nói rõ chỗ nào chưa đo được.** Đây là phần quan trọng nhất của tài liệu này.

---

## 2. Chỉ số cấp 0 — Kỹ thuật (đo tự động, mỗi commit)

Đây là nhóm **duy nhất hiện đang đo được hoàn toàn tự động**. Mỗi giá trị dưới đây đều chạy được bằng một lệnh.

| Chỉ số | Ngưỡng | Lệnh kiểm tra | Nguồn |
| :--- | :--- | :--- | :--- |
| Unit test PASS | **6/6** | `python -m unittest discover -s tests -v` | `tests/test_hello_bridge.py` |
| Demo chạy được | **exit 0** | `python examples/01-hello-agent/hello_bridge.py` | CI `ci.yml` |
| Thời gian demo | **< 60 giây** (thực tế: **0,06 giây**) | đo tại CI | CI `ci.yml` |
| Dependency ngoài stdlib | **0** | `python scripts/license_gate.py` | CI `license.yml` |
| File source thiếu SPDX | **0** | `python scripts/license_gate.py` | CI `license.yml` |
| Package bị chặn (copyleft) | **0** | `python scripts/license_gate.py` | `scripts/license_gate_allowlist.txt` |
| Phiên bản Python tương thích | **3.8 · 3.10 · 3.12** | CI matrix | `ci.yml` |
| Rò rỉ secret phát hiện | **0** | TruffleHog (`--only-verified`) | CI `ci.yml` |

> Tất cả nhóm này hiện đạt. Đây là phần dự án **chắc chắn** nhất — và cũng là phần ít thú vị nhất.
> Phần thú vị nằm ở mục 4.

---

## 3. Chỉ số cấp 1 — Đóng góp cộng đồng (đo thủ công)

| Chỉ số | Mục tiêu 90 ngày | Cách đo | Chu kỳ |
| :--- | :--- | :--- | :--- |
| Issue mới | ≥ 5 | đếm trong tab Issues | tuần |
| Phản hồi Issue | **100% trong 7 ngày** | kiểm thủ công | tuần |
| PR mới (từ cộng đồng) | ≥ 3 | tab Pull Requests | tháng |
| PR được hợp nhất | ≥ 1 | tab Pull Requests | tháng |
| Contributor mới | ≥ 2 | `CONTRIBUTORS` | tháng |
| Người đóng góp đạt Bậc 2 | ≥ 1 | theo [CONTRIBUTOR_LADDER](../../CONTRIBUTOR_LADDER.md) | tháng |
| Issue được gắn `good first issue` | ≥ 3 đầu việc **đủ cụ thể** | kiểm thủ công | tuần |

**Định nghĩa "đủ cụ thể"** (để tránh tính số): một đầu việc chỉ tính nếu có **mô tả vấn đề**, **tên hàm/tệp
liên quan**, **tiêu chí nghiệm thu** và **không cần hỏi thêm**.

---

## 4. Chỗ CHƯA đo được — và vì sao

Phần này tồn tại để bảo đảm tài liệu này **không phải bản khoe doanh thu**.

| Chỉ số hiệu muốn đo | Vì sao chưa đo được | Khi nào sẽ đo được |
| :--- | :--- | :--- |
| **Lượt xem / tiếp cận** (reach, impressions) | Chưa có tài khoản phân tích nào; đều đo thủ công bằng mắt | Sau khi có website + tài khoản phân tích |
| **Mức độ tương tác** (engagement) | Chưa có kênh nào để đo; quy mô hiện tại chưa đủ cho số liệu | Khi có ≥ 1 kênh hoạt động ≥ 1 tháng |
| **Số người dùng thử** | Dự án **không cung cấp dịch vụ** — không có nơi để người dùng đăng ký | Khi có pilot/PoC công khai được công bố |
| **Chất lượng đóng góp** (giữ được ai) | Cần thời gian dài hơn 90 ngày để đo | Sau 6 tháng |
| **Chi phí cơ hội** của người duy trì | Không đo được bằng công cụ | Ghi nhận thủ công trong báo cáo |

> **Chúng tôi không công bố chỉ số không đo được.** Nếu bạn thấy một bài viết quảng cáo "hơn 1.000 lượt tiếp cận"
> cho dự án này, đó **không phải** con số từ dự án — hãy kiểm tra lại nguồn.

---

## 5. Báo cáo

| Loại | Chu kỳ | Hình thức | Gửi đi |
| :--- | :--- | :--- | :--- |
| Báo cáo tuần | **Thứ Sáu** | 5 dòng: Issue mới · Issue đã trả lời · PR mới · Chỉ số kỹ thuật · Việc tuần sau | Issue `meta` + email |
| Báo cáo tháng | **Ngày 28** | Bảng chỉ số cấp 0 + cấp 1 + phần "chỗ chưa đo được" + quyết định cần hỗ trợ | Issue `meta` |
| Báo cáo quý | Quý | Cập nhật sổ rủi ro, roadmap, KPI cấp 1 | Issue `meta` + email |

### Mẫu báo cáo tuần (5 dòng)

```
Tuần 2026-W43 · Issue mới: N · Đã trả lời: N/N · PR mới: N · Hợp nhất: N
Kỹ thuật: test 6/6 PASS · demo exit 0 (0,06s) · license gate exit 0 · 0 rò rỉ secret
Việc tuần sau: <2 dòng>
Cần hỗ trợ: <1 dòng, nếu có>
```

> Nếu một tuần không có gì đáng kể, báo cáo vẫn gửi — **và ghi rõ là không có gì**. Đó là giá trị của
> báo cáo đều đặn: nó cho biết dự án còn sống.

---

## 6. Nguyên tắc dữ liệu

- Dữ liệu thống kê phải **tái lập được** bằng lệnh trong repo.
- Nếu một con số không có lệnh kiểm tra, nó là **ước tính**, và phải được ghi là ước tính.
- Chúng tôi **không** công bố số liệu từ công cụ bên thứ ba mà không nói rõ nguồn.
