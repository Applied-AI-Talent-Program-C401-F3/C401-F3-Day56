# 🏗️ Vai trò: Kỹ sư Kiến trúc (Architecture Developer)

Trong dự án này, tôi đảm nhận vai trò Kỹ sư Kiến trúc. Trách nhiệm chính của tôi là thiết kế luồng xử lý cốt lõi cho AI Agent bằng cách sử dụng thư viện `langgraph`. Đối với phiên bản demo, đồ thị (graph) được thiết kế theo hướng tinh gọn, sử dụng cấu trúc một vòng lặp (single loop) nhằm đảm bảo tính trực quan, dễ theo dõi và dễ gỡ lỗi.

---

# 🚀 Chi tiết Đóng góp (Contributions & Elaboration)

Dưới đây là sự phân tích chuyên sâu về các hạng mục tôi đã thực hiện nhằm biến bản thiết kế kiến trúc thành một hệ thống hoạt động thực tế:

## 1. Thiết kế "Công cụ" cho Agent (Tool Provisioning)
* **Những gì tôi làm:** Tôi chịu trách nhiệm định nghĩa và xây dựng logic cho bộ công cụ (tools) cho LangGraph để AI Agent có thể gọi và sử dụng khi cần thiết.
* **Phân tích:** Nếu LangGraph là "bộ não" điều hướng logic, thì các công cụ chính là "đôi tay" của hệ thống. Đóng góp này biến một LLM (chỉ biết sinh văn bản) thành một thực thể có khả năng hành động (Agentic AI). Bằng cách chuẩn hóa đầu vào và đầu ra của các công cụ, tôi đảm bảo đồ thị có thể nhận diện chính xác công cụ nào cần được gọi trong từng ngữ cảnh cụ thể.

## 2. Kiểm soát Luồng và Điều kiện Dừng (Smart Termination Logic)
* **Những gì tôi làm:** Thiết lập logic kiểm tra: Nếu Agent thu thập đủ thông tin cần thiết từ các công cụ (hoặc từ câu hỏi gốc), vòng lặp sẽ kết thúc (chuyển sang node `END`). Câu trả lời sau đó được tổng hợp và gửi trực tiếp đến người dùng dưới dạng phiên bản hoàn chỉnh cuối cùng.
* **Phân tích:** Đây là yếu tố sống còn của một hệ thống Agent. Việc thiếu điều kiện dừng tối ưu thường dẫn đến lỗi "vòng lặp vô tận" (Agent liên tục gọi tool một cách kẹt cứng). Thiết kế của tôi giúp hệ thống tiết kiệm chi phí token (API cost), giảm thiểu thời gian chờ đợi (latency) cho người dùng, và đảm bảo câu trả lời đưa ra luôn mạch lạc, dứt khoát chứ không bị cắt xén giữa chừng.

## 3. Thiết lập Hàng rào Bảo mật (Prompt Injection Guardrails)
* **Những gì tôi làm:** Xây dựng cơ chế phòng vệ chống lại các rủi ro bảo mật (như Prompt Injection hay Jailbreak) bằng cách thiết kế một System Prompt (Hệ thống Chỉ thị gốc) chặt chẽ và an toàn.
* **Phân tích:** Người dùng cuối có thể nhập bất cứ thứ gì, kể cả những câu lệnh cố ý đánh lừa AI để phá vỡ quy tắc của ứng dụng. Dưới góc độ kiến trúc, việc nhúng một "vòng bảo vệ" ngay từ lớp System Prompt giúp Agent kiên định với vai trò của mình, tự động từ chối các yêu cầu vi phạm chính sách hoặc nguy hiểm mà không làm sập luồng của LangGraph.

## 4. Xây dựng Tài liệu Kỹ thuật (Documentation / README)
* **Những gì tôi làm:** Viết và hoàn thiện file `README.md` cho toàn bộ dự án.
* **Phân tích:** Mã nguồn kiến trúc (như LangGraph) có thể rất trừu tượng đối với người mới tiếp cận. Việc soạn thảo tài liệu rõ ràng giúp giải thích cấu trúc các node/edge, cách cài đặt môi trường, và cách kích hoạt vòng lặp demo. Nó chứng minh tư duy của một lập trình viên chuyên nghiệp: code tốt phải đi kèm với tài liệu tốt để đảm bảo khả năng bàn giao và mở rộng trong tương lai.