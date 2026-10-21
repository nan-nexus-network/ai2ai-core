# Lộ Trình Vai Trò Trong Cộng Đồng (Contributor Ladder)

Sáng kiến **NAN AI2AI-SI2SI** được khởi xướng bởi một cá nhân không chuyên về lập trình, vì vậy sức sống thực sự của dự án phụ thuộc vào các kỹ sư, nhà nghiên cứu và chuyên gia tham gia kiểm chứng.

Chúng tôi thiết lập 3 bậc tham gia minh bạch dựa trên đóng góp thực chất (không phân biệt bằng cấp, tuổi tác hay việc bạn chọn dùng tên thật hay biệt danh):

```
[Bậc 1: Contributor] ──> [Bậc 2: Module Reviewer] ──> [Bậc 3: Core Maintainer]
(Đóng góp đầu tiên)       (Đóng góp & Review ổn định)   (Đồng quản trị & Tiếp nhận bàn giao)
```

---

## 🌱 Bậc 1: Người Đóng Góp Cộng Đồng (Community Contributor)
* **Điều kiện đạt được:**
  * Có ít nhất **01 Pull Request (PR)** được chấp thuận (sửa lỗi code, thêm unit test, dịch tài liệu, sửa lỗi chính tả), **HOẶC**
  * Mở **01 Issue phản biện chất lượng** chỉ ra lỗ hổng logic/bảo mật trong Tài liệu thảo luận hoặc trong mã nguồn PoC.
* **Quyền lợi & Ghi nhận:**
  * Được ghi tên/biệt danh vĩnh viễn vào danh sách đóng góp của dự án.
  * Được mời vào nhóm thảo luận kỹ thuật nòng cốt.

---

## 🛠 Bậc 2: Người Phản Biện & Phụ Trách Mô-đun (Reviewer / Module Maintainer)
* **Điều kiện đạt được:**
  * Có từ **03 PR kỹ thuật hoặc tài liệu chuyên sâu** được hợp nhất vào nhánh chính.
  * Tham gia hỗ trợ giải đáp hoặc kiểm tra (review) code cho các thành viên mới một cách văn minh, mang tính xây dựng.
* **Quyền hạn & Trách nhiệm:**
  * Được cấp quyền **Triage** trên GitHub Repository (gắn nhãn Issue, đóng Issue trùng lặp, đề xuất duyệt PR).
  * Đứng tên phụ trách kỹ thuật cho một mô-đun cụ thể (ví dụ: *Security & Sanitizer*, *Cryptography Receipt*, hoặc *ASEAN Policy Mapping*).

---

## 🏛 Bậc 3: Hội Đồng Duy Trì Cốt Lõi (Core Maintainer)
* **Điều kiện đạt được:**
  * Có đóng góp kiến trúc quan trọng trong tối thiểu **60 ngày** và được các thành viên Bậc 2 đồng thuận đề cử.
* **Quyền hạn & Trách nhiệm:**
  * Quyền phê duyệt và hợp nhất trực tiếp (Write / Maintain Access) vào nhánh `main` và phát hành các phiên bản Release mới (`v0.2`, `v0.3`...).
  * Quyền biểu quyết định hướng kiến trúc của giao thức và cập nhật các phiên bản tiếp theo của Tài liệu thảo luận (White Paper).
  * **Quyền ưu tiên tiếp quản dự án:** Theo cam kết tại [HANDOVER.md](HANDOVER.md), nếu người khởi xướng dừng hoạt động sau 12 tháng, các thành viên Bậc 3 sẽ là những người đầu tiên được trao toàn quyền quản trị cao nhất (Admin Organization) để tiếp quản và đồng hành phát triển dự án.

---

## Nguyên Tắc Làm Việc Chung
1. **Không ép buộc thời gian:** Mọi đóng góp đều hoàn toàn tự nguyện. Bạn có thể tạm nghỉ hoặc rút lui bất kỳ lúc nào.
2. **Tranh luận vào vấn đề, không công kích cá nhân:** Mọi phản biện gay gắt về kỹ thuật đều được hoan nghênh; mọi sự thiếu tôn trọng cá nhân đều bị từ chối.
