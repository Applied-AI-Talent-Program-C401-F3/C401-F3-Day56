# User Stories và Path: AI Doctor Booking

# Đúng:
- AI hỏi đầy đủ thông tin của người dùng khi đặt bác sỹ: Triệu chứng, chọn Vinmec ở thành phố nào, có yêu cầu gì đặc biệt với bác sỹ, giá cả tư vấn dự kiến

# Sai:
- AI có thể tự bịa ra các thông tin về bác sỹ, hoặc không có guardrail cụ thể khi người sử dụng lạm dụng Chatbot. Thứ tự yêu cầu gọi tool: Triệu chứng->Thành phố->Tầm giá->Yêu cầu bác sỹ.
- Nếu AI gọi bác sỹ trước -> tốn token gọi tool mà bác sỹ không đúng chuyên môn hoặc không đúng yêu cầu

# Không chắc:
- Nếu không đủ thông tin -> AI cần tìm hiểu đầy đủ thông tin từ người dùng, nếu không chắc cần hỏi lại cho đủ
- Nếu vẫn không đảm bảo thông tin từ người dùng mà quá số vòng lặp -> Không đáp ứng

# Mất tin
- Cần có bộ nhớ trong trường hợp kết nối không ổn định hoặc drop session


# Đặc tả Yêu cầu Hệ thống (System Specifications): AI Doctor Booking Agent - Vinmec

## 1. Nhánh Đúng (Happy Path - Luồng Chuẩn)
**Mô tả kỹ thuật:** Agent State cần định nghĩa 4 biến bắt buộc: `symptoms` (triệu chứng), `location` (thành phố/cơ sở Vinmec), `budget` (ngân sách/tầm giá), và `preferences` (yêu cầu đặc biệt về bác sĩ). AI sẽ linh hoạt trích xuất thông tin này từ câu nói tự nhiên của người dùng.

**User Stories:**
* **US1.1:** Là một người dùng, tôi muốn AI chủ động hỏi tôi các thông tin còn thiếu (triệu chứng, địa điểm, tầm giá, yêu cầu đặc biệt) một cách tự nhiên và logic để đặt đúng bác sĩ.
* **US1.2:** Là một người dùng, tôi muốn nhận được danh sách tóm tắt các bác sĩ Vinmec phù hợp nhất, kèm theo chi tiết chuyên môn và lịch trống, sau khi đã cung cấp đủ thông tin.
* **US1.3:** Là một hệ thống, tôi muốn gom nhóm các câu hỏi (ví dụ: hỏi địa điểm và tầm giá cùng lúc) nếu phù hợp, để giảm thiểu số bước giao tiếp của người dùng.

---

## 2. Nhánh Sai (Bad/Error Path - Luồng Xử lý Ngoại lệ & Lạm dụng)
**Mô tả kỹ thuật:**
Yêu cầu các Node kiểm duyệt (Guardrails) và luồng điều hướng (Routing) chặt chẽ trong LangGraph. Phải thiết lập Conditional Edges để đảm bảo Node `Call_Vinmec_API` chỉ chạy khi 4 biến State đã có giá trị. Đồng thời, cấu hình System Prompt để kiểm soát hiện tượng ảo giác (Hallucination).

**User Stories:**
* **US2.1:** Là một quản trị viên hệ thống, tôi muốn AI từ chối trả lời (Fallback) khi người dùng nhập các câu lệnh nằm ngoài phạm vi y tế, yết giá, hoặc cố tình lạm dụng/đánh lừa (Prompt Injection) chatbot.
* **US2.2:** Là một kỹ sư tối ưu chi phí, tôi muốn hệ thống CHỈ gọi Tool tìm kiếm bác sĩ theo đúng thứ tự điều kiện lọc: `Triệu chứng -> Thành phố -> Tầm giá -> Yêu cầu` để tiết kiệm Token và tránh truy vấn cơ sở dữ liệu lãng phí.
* **US2.3:** Là một người dùng, tôi muốn mọi thông tin về bác sĩ do AI cung cấp phải chính xác 100% từ dữ liệu thực tế của Vinmec, tuyệt đối không được tự bịa ra (Hallucination) tên tuổi hay chuyên môn sai lệch.

---

## 3. Nhánh Không Chắc (Uncertain/Edge Path - Luồng Mập Mờ)
**Mô tả kỹ thuật:**
Xử lý các truy vấn thiếu ngữ cảnh hoặc quá rộng (ví dụ: "Tôi bị mệt"). Agent cần một công cụ (Tool) phân tích triệu chứng sơ bộ để hỏi lại người dùng. Cần thiết lập biến `retry_count` trong State để giới hạn số vòng lặp hỏi đáp cho một trường thông tin.

**User Stories:**
* **US3.1:** Là một người dùng, nếu tôi mô tả triệu chứng quá chung chung, tôi muốn AI đặt các câu hỏi trắc nghiệm hoặc gợi ý phụ để giúp tôi xác định rõ hơn chuyên khoa cần khám.
* **US3.2:** Là một hệ thống, tôi muốn giới hạn số lần hỏi lại (ví dụ: tối đa 3 vòng lặp) khi không thể trích xuất được thông tin hợp lệ từ người dùng.
* **US3.3:** Là một người dùng, nếu AI không thể hiểu nhu cầu của tôi sau nhiều lần hỏi lại, tôi muốn được chuyển tiếp kết nối đến nhân viên chăm sóc khách hàng là con người (Human Handoff) để tiếp tục hỗ trợ.

---

## 4. Nhánh Mất Tin (Lost/Drop Session Path - Luồng Khôi Phục)
**Mô tả kỹ thuật:**
Yêu cầu tích hợp bộ nhớ dài hạn (Memory/Checkpointing) thông qua cơ chế `thread_id` của LangGraph. Hệ thống phải lưu trữ State hiện tại của người dùng vào cơ sở dữ liệu (Redis/PostgreSQL) sau mỗi lượt tương tác.

**User Stories:**
* **US4.1:** Là một người dùng, nếu tôi bị mất kết nối mạng hoặc vô tình đóng ứng dụng giữa chừng, tôi muốn hệ thống nhớ lại các thông tin tôi đã cung cấp trước đó (triệu chứng, địa điểm...) khi tôi quay lại.
* **US4.2:** Là một hệ thống, tôi muốn gửi một tin nhắn chào mừng theo ngữ cảnh (ví dụ: "Chào bạn quay lại, chúng ta đang dở dang việc tìm bác sĩ tiêu hóa tại Hà Nội...") khi phát hiện phiên (session) bị gián đoạn được kết nối lại.