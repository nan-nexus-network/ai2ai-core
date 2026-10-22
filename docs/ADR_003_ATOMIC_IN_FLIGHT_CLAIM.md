# ADR-003: Atomic In-flight Claim — chống thực thi lặp đồng thời

**Ngày:** 22/10/2026 · **Trạng thái:** Đã chấp nhận (Accepted) · **Bổ sung cho:** `docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md`
**Mã:** v0.2.1-dev

---

## 1. Bối cảnh

Một kỹ sư hệ thống chỉ ra lỗ hổng trong cơ chế idempotency của v0.2:

> Nếu 2 request có cùng `operation_id` đến **cùng lúc**, cả hai đều thấy cache rỗng và cùng thực thi.

Đây là **race condition** (TOCTOU — time-of-check to time-of-use). Kiểm tra cache đơn thuần chỉ bảo vệ được trường hợp **tuần tự**: request thứ hai đến sau khi request thứ nhất đã ghi kết quả.

**Hậu quả:** với tác vụ có tính phí — thanh toán, đặt hàng, gọi API trả tiền, phát hành vé — đây là **double-spend**. Việc tác vụ chạy hai lần có thể **không thể hoàn tác**.

## 2. Vì sao không đủ nếu chỉ khoá ở bước cấp biên nhận

Nếu cơ chế chỉ kiểm tra cache **sau khi** tác vụ đã chạy (tức ở bước cấp biên nhận), thì request thứ hai vẫn **đã gọi tác vụ** rồi mới phát hiện trùng và nhận lại kết quả cũ. Tác vụ đã chạy hai lần.

Vì vậy **khoá phải được giành trước khi gọi tác vụ**. Đây là điểm khác biệt cốt lõi giữa "deduplication ở bước ghi kết quả" và "claim nguyên tử ở bước thực thi".

## 3. Quyết định

**Dùng "Atomic In-flight Claim":** request đầu tiên **chiếm** (claim) khoá `operation_id` trước khi thực thi; những request sau thấy khoá đang được giữ thì **chờ** (`threading.Event`) thay vì tự chạy.

Cơ chế nằm trong `nan_ai2ai/idempotency.py` (`IdempotencyStore`), dùng **chỉ thư viện chuẩn Python**:

| Thành phần | Vai trò |
|:---|:---|
| `threading.Lock` (`_cache_lock`) | Bảo vệ **mọi** biến đổi trạng thái. Chỉ giữ khoá trong thời gian ngắn. |
| `threading.Event` (`_in_flight_events`) | Một Event cho mỗi `operation_id` đang xử lý. Request chờ gọi `event.wait()` **ngoài khoá**. |
| `_receipt_cache` | `operation_id` → `{"status": "PROCESSING"\|"DONE"\|"FAILED", ...}` |

### Ba trạng thái

| Trạng thái | Ý nghĩa | Hành vi của request sau đó |
|:---|:---|:---|
| `PROCESSING` | Khoá đã được chiếm, tác vụ đang chạy | **Chờ** `event.wait()`, rồi quay lại đọc trạng thái |
| `DONE` | Đã có kết quả | Trả lại kết quả cũ (log `Duplicate detected! Returning cached receipt.`) |
| `FAILED` | Lần chạy trước đã lỗi | Ném lỗi ra cho caller — **không** tự chạy lại |

### Quy tắc "at-most-once", và vì sao lỗi thì **không** tự chạy lại

Cùng một `operation_id` chỉ được thực thi **đúng một lần**. Nếu lần chạy đó lỗi, khoá được đánh dấu `FAILED` và những request đang chờ **nhận lỗi đó**, không tự động chạy lại.

**Lý do:** tác vụ có thể **đã** có tác dụng phụ (đã trừ tiền, đã gửi hàng, đã gọi API trả phí) trước khi lỗi xảy ra. Chạy lại tự động là **mở lại đúng lỗi double-spend** mà cơ chế này sinh ra để chống. Ưu tiên an toàn tài chính hơn thuận tiện.

Đánh đổi: một thao tác lỗi sẽ **không** tự retry. Người gọi phải dùng `operation_id` mới để thử lại — và phải tự biết tác vụ cũ đã hỏng ở đâu.

## 4. Vì sao dùng `threading.Event` chứ không dùng `Condition`

`threading.Condition` có thể làm lộ thứ tự FIFO giữa các waiter, nhưng `Event` đơn giản hơn và **không** đảm bảo thứ tự — mà thứ tự không quan trọng ở đây: mọi waiter đều nhận **cùng một** kết quả.

Quan trọng hơn: sau `event.wait()` trả về, code **phải quay lại đọc trạng thái** (vòng lặp `while True`), **không** được giả định kết quả đã có. Lý do: request chờ có thể thức dậy khi lần chạy kia **vừa thất bại** (trạng thái `FAILED`), hoặc `Event` bị đánh thức mà ghi kết quả chưa kịp nhìn thấy. Vòng lặp xử lý cả hai.

## 5. Giới hạn (PoC) — nói rõ, không giấu

| Giới hạn | Hệ quả |
|:---|:---|
| Trạng thái **chỉ trong bộ nhớ một tiến trình** | Mất khi khởi động lại. **Không** dùng chung giữa nhiều tiến trình/nút. |
| `threading.Lock` chỉ bảo vệ **trong một tiến trình Python** | Nhiều tiến trình hoặc nhiều máy vẫn race → cần khoá phân tán (Redis, v.v.) |
| **Không có TTL** | Mục đích vô hạn nếu không dọn |
| `Event.wait()` **không** bảo đảm FIFO | Không ảnh hưởng: mọi waiter nhận cùng một kết quả |
| Chưa có **ghi log audit** cho mỗi lần claim | Không truy vết được ai đã claim khoá khi nào |

## 6. Vì sao đặt engine vào gói `nan_ai2ai` thay vì nhân bản trong từng demo

`examples/01-hello-agent/hello_bridge.py` và `examples/02-agent-to-agent-chat/agent_chat.py` là **hai hiện thực bridge độc lập** (xem `ROADMAP.md`, mục BL4). Nếu mỗi file có một bản riêng của cơ chế khoá, logic sẽ **trôi khỏi nhau** — và đó chính xác là loại lỗi đã xảy ra với `source_ref` trong kho `ai2ai-research`.

Vì vậy logic nằm trong `nan_ai2ai/idempotency.py`; mỗi bridge dùng **kho riêng** (đúng như trước, để không lẫn biên nhận giữa hai schema khác nhau) nhưng **cùng một bộ máy**. Ba thuộc tính `_cache_lock`, `_in_flight_events`, `_receipt_cache` được expose trên lớp bridge đúng như đặc tả, và chúng **là cùng đối tượng** với thuộc tính bên trong store — nên có thể kiểm tra/xoá trực tiếp trong test mà không lệch logic.

## 7. Bằng chứng

| Kiểm chứng | Kết quả |
|:---|:---|
| `test_12_concurrent_idempotency` | 2 thread, cùng `operation_id`, tác vụ ngủ 1s → tác vụ chạy **đúng 1 lần**, cả hai nhận **cùng `receipt_id`** |
| `test_12b_concurrent_failure_is_not_retried_automatically` | Tác vụ lỗi → cả hai nhận lỗi, tác vụ **không** chạy lại, trạng thái `FAILED` |
| `test_12c_distinct_operations_run_concurrently` | Hai `operation_id` khác nhau → chạy **song song**, không chặn nhau, 2 biên nhận khác nhau |
| Toàn bộ bộ test | **124 test PASS** (trước: 121) |
| Demo `agent_chat.py` | Bob thực thi **1 lần** dù Alice gửi 2 lần |

## 8. Những gì quyết định này **không** làm

- Không biến thành cơ chế idempotency **phân tán** — vẫn là một tiến trình.
- Không thêm dependency nào (chỉ `threading` của thư viện chuẩn).
- Không hợp nhất hai hiện thực bridge (vẫn là BL4).
- Không thay đổi ngữ nghĩa của biên nhận `nan-receipt/v1` ở `ADR-002`.
