# Trợ Lý AI Đặt Lịch Khám Bệnh Vinmec 🏥🤖

Một trợ lý AI đàm thoại được xây dựng bằng [LangGraph](https://python.langchain.com/docs/langgraph), thiết kế để tư vấn và hỗ trợ người dùng đặt lịch hẹn y tế tại hệ thống bệnh viện Vinmec. Trợ lý này thu thập nhu cầu của người dùng một cách thông minh, áp dụng các rào cản (guardrails) nghiêm ngặt để ngăn chặn tình trạng ảo giác (hallucination) và quản lý trạng thái, bộ nhớ hội thoại để đảm bảo trải nghiệm đặt lịch liền mạch nhất.

---

## 🌟 Tính Năng Chính

Dự án này được xây dựng xoay quanh Kiến trúc 4 Luồng (4-Path Architecture) mạnh mẽ:

### 1. Nhánh Đúng (Luồng Chuẩn - Slot-Filling)
* **Luồng Giao Tiếp Tự Nhiên:** Thu thập thông tin bắt buộc (`Triệu chứng`, `Địa điểm`, `Ngân sách`, `Yêu cầu Bác sĩ`) một cách tự nhiên qua hội thoại, không hỏi cứng nhắc như một bản khảo sát.
* **Tổng Hợp Thông Minh:** Có khả năng hiểu nhiều tham số trong cùng một câu nói (Ví dụ: *"Tôi bị đau đầu và muốn tìm bác sĩ ở Hà Nội giá dưới 500k"*).

### 2. Nhánh Sai (Luồng Ngoại Lệ & Tối Ưu Chi Phí)
* **Không Ảo Giác (Zero Hallucination):** System prompt nghiêm ngặt đảm bảo AI chỉ gợi ý các bác sĩ có thật được truy xuất từ API dữ liệu của Vinmec. AI tuyệt đối không tự bịa ra tên, chuyên môn hay lịch khám.
* **Tối Ưu Token/Chi Phí:** Ép buộc một quy trình gọi Tool nghiêm ngặt (`Triệu chứng -> Thành phố -> Tầm giá -> Yêu cầu`). Tool truy vấn database CHỈ được kích hoạt khi tất cả các biến bắt buộc đã được điền đầy đủ.
* **Kiểm Duyệt Đầu Vào (Guardrails):** Tự động chặn các truy vấn không liên quan đến y tế, các nỗ lực tấn công prompt (prompt injection) hoặc lạm dụng hệ thống.

### 3. Nhánh Không Chắc (Luồng Mập Mờ & Xử Lý Chuyển Tiếp)
* **Cơ Chế Làm Rõ:** Nếu người dùng cung cấp các triệu chứng quá chung chung (ví dụ: "Tôi thấy mệt"), AI sẽ đưa ra các câu hỏi trắc nghiệm mang tính chẩn đoán sơ bộ để thu hẹp phạm vi chuyên khoa.
* **Chống Vòng Lặp Vô Tận:** Theo dõi biến `retry_count` trong State. Nếu AI không thể lấy được thông tin hợp lệ sau một số lần thử nhất định (ví dụ: 3 lần), hệ thống sẽ chủ động chuyển kết nối cho nhân viên là con người (Human Handoff).

### 4. Nhánh Mất Tin (Luồng Khôi Phục)
* **Bộ Nhớ Bền Bỉ:** Sử dụng cơ chế Checkpointing của LangGraph (qua Redis/PostgreSQL hoặc SQLite cho môi trường dev) kết hợp với `thread_id` để lưu trữ trạng thái cuộc trò chuyện.
* **Khôi Phục Khi Rớt Mạng:** Nếu người dùng bị mất kết nối hoặc tải lại trang, AI sẽ nhớ các chi tiết đã cung cấp trước đó và tiếp tục đúng ngữ cảnh (Ví dụ: *"Chào bạn quay lại! Chúng ta đang dở dang việc tìm bác sĩ tiêu hóa tại Hà Nội..."*).

---

## 🏗️ Kiến Trúc & LangGraph State

### Cấu Trúc State của Agent
Đồ thị (Graph) dựa vào một `TypedDict` State chung để theo dõi hội thoại và logic điều hướng:

```python
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class BookingState(TypedDict):
    messages: List[BaseMessage]
    symptoms: Optional[str]
    location: Optional[str]
    budget: Optional[str]
    preferences: Optional[str]
    retry_count: int
    tool_called: bool
```
