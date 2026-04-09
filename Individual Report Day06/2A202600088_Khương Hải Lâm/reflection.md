# Reflection - 2A202600088 Khương Hải Lâm

## 1) Role cụ thể trong nhóm
Mình đảm nhận vai trò **Kỹ sư Kiến trúc (Architecture Developer)**: chịu trách nhiệm thiết kế luồng xử lý cốt lõi cho AI Agent bằng thư viện `langgraph`. Đối với phiên bản demo, mình đảm bảo đồ thị (graph) hoạt động trơn tru với cấu trúc một vòng lặp (single loop) tinh gọn, nhằm đảm bảo tính trực quan, dễ theo dõi và dễ gỡ lỗi.

## 2) Phần phụ trách cụ thể (2-3 đóng góp có output rõ)
1. **Thiết kế và cung cấp "Công cụ" cho Agent (Tool Provisioning)**
   - Output rõ: Định nghĩa logic bộ công cụ (tools) để tích hợp vào LangGraph, chuẩn hóa đầu vào/đầu ra giúp LLM (Agentic AI) có thể nhận diện và gọi chính xác công cụ cần thiết trong từng ngữ cảnh.
2. **Kiểm soát luồng và điều kiện dừng (Smart Termination Logic)**
   - Output rõ: Logic code điều hướng chuyển sang node `END` khi Agent đã thu thập đủ thông tin. Điều này giúp ngăn chặn lỗi "vòng lặp vô tận", tối ưu chi phí token (API cost), giảm latency và đảm bảo câu trả lời dứt khoát.
3. **Xây dựng tài liệu kỹ thuật (Documentation)**
   - Output rõ: File `README.md` hoàn chỉnh cho dự án, giải thích chi tiết cấu trúc các node/edge, cách cài đặt môi trường và cách kích hoạt luồng chạy demo để dễ dàng bàn giao.

## 3) Kiến trúc/Phân luồng phần nào mạnh nhất, phần nào yếu nhất? Vì sao?
- **Mạnh nhất:** Phần kiểm soát luồng điều kiện dừng (Termination Logic).
  - Vì cấu trúc single-loop được định nghĩa ranh giới rất rõ, Agent biết chính xác khi nào cần dừng việc gọi tool để trả kết quả cho user, tránh tình trạng kẹt cứng hoặc sinh ra log rác.
- **Yếu nhất:** Khả năng xử lý lỗi ngoại lệ (Error handling & Fallback) của các công cụ.
  - Vì tập trung làm luồng demo tinh gọn nhanh nhất có thể, đồ thị hiện tại chưa có các node rẽ nhánh phức tạp để tự động thử lại (retry) hoặc dùng tool dự phòng nếu API của một tool bất ngờ bị sập (downtime).

## 4) Đóng góp cụ thể khác với mục 2
- Thiết lập **hàng rào bảo mật (Prompt Injection Guardrails)** thông qua việc tinh chỉnh System Prompt gốc. Qua đó, giúp Agent kiên định với vai trò, tự động từ chối các yêu cầu độc hại/jailbreak từ người dùng mà không làm đứt gãy luồng của LangGraph.
- Hỗ trợ nhóm debug trực tiếp các node trong quá trình chạy thử để đảm bảo dữ liệu (state) được truyền đi chính xác giữa các bước.

## 5) 1 điều học được trong hackathon mà trước đó chưa biết
Mình học được cách tư duy quản lý trạng thái (state management) thực tế trong `langgraph`. Việc xây dựng AI Agent không chỉ đơn thuần là gửi prompt và nhận text, mà là thiết kế một "đồ thị trạng thái" nơi dữ liệu, lịch sử gọi tool và quyết định của LLM phải được lưu trữ, luân chuyển nhịp nhàng giữa các node để hệ thống không bị "mất trí nhớ".

## 6) Nếu làm lại, đổi gì? (cụ thể)
Nếu làm lại, mình sẽ:
1. Thiết kế thêm cơ chế **Human-in-the-loop (HITL)** cho một số tool nhạy cảm, cho phép đồ thị tạm dừng (pause) để chờ người dùng xác nhận trước khi tiếp tục thực thi.
2. Xây dựng một bộ **Mock Data Tools** (công cụ trả về dữ liệu giả) ngay từ đầu để test luồng graph mượt mà hơn, thay vì phải gọi API thật liên tục gây tốn kém và chậm trễ trong khâu gỡ lỗi.

## 7) AI giúp gì? AI sai/mislead ở đâu?
- **AI giúp:**
  - Viết nhanh các đoạn boilerplate code để khởi tạo các node và edge cơ bản trong LangGraph.
  - Hỗ trợ rà soát lỗi cú pháp và format lại file `README.md` từ dàn ý thô sơ thành một tài liệu chuẩn chỉnh, chuyên nghiệp.
- **AI sai/mislead:**
  - AI thường xuyên gợi ý code sử dụng các hàm hoặc syntax của phiên bản LangChain/LangGraph cũ (đã deprecated), khiến code bị lỗi khi chạy và mình phải tự tìm đọc document mới nhất để sửa.
  - Đôi khi AI vẽ ra các cấu trúc đồ thị (multi-agent, nested sub-graphs) quá mức phức tạp so với yêu cầu tinh gọn của dự án, làm mất thời gian nếu cứ đi theo hướng dẫn đó.