# Lộ Trình Công Khai (Public Roadmap)

**Phiên bản:** v1.0 · **Cập nhật:** 21/10/2026

> Lộ trình này mô tả **những gì dự án đang cố làm và không làm**. Nó không phải lịch trình cam kết.
> Mọi mốc đều có thể đổi; điều được giữ là **phạm vi** và **nguyên tắc minh bạch**.

---

## Nguyên tắc điều hành lộ trình

1. **Không hứa ngày tháng khi chưa có bằng chứng.** Các mốc ghi "chưa cam kết" là chủ ý.
2. **Minh bạch trước, phát hành sau.** Không công bố tính năng chưa chạy được.
3. **Mọi phát hành đều đi kèm bằng chứng kiểm thử** (CI xanh, mã băm kiểm chứng).

---

## Giai đoạn hiện tại: `v0.1` · Hộp cát thử nghiệm (Sandbox)

| Hạng mục | Trạng thái |
| :--- | :--- |
| Mã PoC 60 giây + 10 unit test | ✅ **Hoàn tất** |
| Tài liệu thảo luận mở (7 chương, 12 câu hỏi mở) | ✅ **Hoàn tất** (`v0.4-draft`) |
| Khung pháp lý (LICENSE, CLA, TRADEMARK, HANDOVER) | ✅ Hoàn tất |
| CI: quét secret + test 3 phiên bản Python + license gate | ✅ Hoàn tất |
| Cổng kiểm định 4 cấp độ (4 Cổng) + lộ trình vai trò | ✅ Hoàn tất |
| **Phát hành ra công khai** | ⏳ **Đang chờ** (xem checklist [docs/public_launch/06_RELEASE_CHECKLIST.md](docs/public_launch/06_RELEASE_CHECKLIST.md)) |

## Giai đoạn kế tiếp: `v0.2` · Mở rộng cộng đồng kỹ thuật

| Hạng mục | Trạng thái |
| :--- | :--- |
| Nhận ≥ 3 Pull Request đóng góp đầu tiên từ cộng đồng | ⏳ Chưa có |
| Bổ sung ≥ 5 unit test cho luồng dịch MCP → A2A (Issue #3) | ⏳ Chưa có |
| Thay blocklist từ khóa bằng kiểm tra cấu trúc an toàn (Issue #1) | ⏳ Chưa có |
| Chữ ký bất đối xứng Ed25519 cho biên nhận xác thực (Issue #2) | ⏳ Chưa có |
| Chuyển tài liệu thảo luận sang **CC-BY 4.0**, mở bản dịch tóm tắt tiếng Anh | ⏳ Chưa có |
| Báo cáo KPI công khai đầu tiên | ⏳ Chưa có (xem [docs/public_launch/03_METRICS_AND_MEASUREMENT.md](docs/public_launch/03_METRICS_AND_MEASUREMENT.md)) |

## Giai đoạn sau: `v0.3` · Hộp cát thử nghiệm có người dùng thật

| Hạng mục | Trạng thái |
| :--- | :--- |
| ≥ 5 người dùng thử đã ký dùng gói PoC | ⏳ Chưa có |
| ≥ 1 đối tác tổ chức đã ký MOU | ⏳ Chưa có |
| ≥ 1 bài báo chuyên môn đưa tin | ⏳ Chưa có |
| Sổ rủi ro công khai được cập nhật hằng quý | ⏳ Chưa có |

## Giai đoạn dài hạn: `v1.0` · Chuẩn tham chiếu

| Hạng mục | Trạng thái |
| :--- | :--- |
| Được tham chiếu trong tài liệu kỹ thuật của bên thứ ba | ⏳ Chưa có |
| Tái phân phối lại bởi ít nhất 1 tổ chức độc lập | ⏳ Chưa có |
| Chuyển giao quản trị cho cộng đồng | ⏳ Chưa có (xem cam kết 12 tháng tại [HANDOVER.md](HANDOVER.md)) |

---

## Những gì dự án **không** làm

Để tránh hiểu nhầm, đây là những điều nằm **ngoài** phạm vi:

- ❌ Không cung cấp dịch vụ, API hay hạ tầng chạy thật.
- ❌ Không thu thập, lưu trữ hay xử lý dữ liệu cá nhân của người dùng.
- ❌ Không phát hành token, không bán khóa học, không nhận tiền cho mã nguồn.
- ❌ Không tuyên bố là tiêu chuẩn chính thức của bất kỳ tổ chức nào.
- ❌ Không đại diện cho cộng đồng AI Việt Nam.
