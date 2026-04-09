# Individual reflection — Lưu Lê Gia Bảo - 2A202600118

## 1. Role

DevOps & Presentation. Quản lý môi trường triển khai, cấu hình CI/CD pipeline, theo dõi chi phí/hiệu suất hệ thống và đảm nhiệm vai trò thuyết trình chính (pitching) để ra mắt sản phẩm.

## 2. Đóng góp cụ thể

Về DevOps: Khởi tạo và quản lý repository, thiết lập môi trường Python/LangGraph, cấu hình file `.env` để bảo mật API key. Xây dựng cơ chế logging cơ bản để theo dõi tỷ lệ drop-off (rớt luồng) và tính toán chi phí token (token cost) cho mỗi phiên chat của GPT-4o-mini, giúp team đo lường được hiệu quả kinh tế.

Về Presentation: Lên kịch bản và thiết kế slide thuyết trình (sử dụng Gamma AI để tối ưu thời gian). Truyền tải rõ ràng giá trị cốt lõi của Kiến trúc 4 Luồng (4-Path Architecture) và trình bày bản demo thực tế trước hội đồng, xử lý các câu hỏi Q&A liên quan đến tính khả thi và an toàn y tế.

## 3. SPEC mạnh/yếu

- Điểm mạnh nhất (Eval Metrics & ROI): Phần định nghĩa các chỉ số đo lường (Medical Intent Recall, Booking Conversion Rate) và đặc biệt là ngưỡng dừng (Kill Criteria: Cost > Benefit trong 3 tháng) rất thực tế. Nó chứng minh nhóm không chỉ làm kỹ thuật mà còn có tư duy kinh doanh (business mindset) rõ ràng.
- Điểm yếu nhất (Feasibility/System Architecture): Cấu trúc hiện tại chủ yếu tập trung vào logic Agent (LangGraph), nhưng SPEC chưa đề cập sâu đến cơ chế xử lý tải cao (high concurrency) hoặc giới hạn request (rate limiting) nếu triển khai diện rộng. Dù là prototype, việc thiếu vắng các kịch bản chịu tải khiến rủi ro "sập hệ thống do bạo lượng truy cập" chưa được đánh giá đầy đủ.

## 4. Đóng góp khác

- Hỗ trợ thành viên Lương Trung Kiên (Tool Engineer) và Thái Doãn Minh Hải (Database Engineer) thiết lập môi trường test local và xử lý các lỗi xung đột thư viện (dependency conflicts) trong `requirements.txt`.
- Đóng góp ý kiến cho luồng "Lost/Drop Session Path" của Đặng Tuấn Anh, đảm bảo cơ chế Checkpointing của LangGraph lưu trữ và gọi lại `thread_id` trơn tru khi giả lập kịch bản người dùng rớt mạng.

## 5. Điều học được

Qua dự án này, tôi nhận ra DevOps cho ứng dụng AI (LLMOps) có những đặc thù rất khác biệt so với phần mềm truyền thống. Thay vì chỉ quan tâm đến CPU, RAM hay thời gian phản hồi (latency), tôi phải làm quen với việc giám sát "Token Cost" và "Hallucination Rate".
Về mặt trình bày, tôi học được rằng khi demo một sản phẩm có tính phi định định (non-deterministic) như AI LLM, việc chuẩn bị sẵn các kịch bản xử lý lỗi (fallback) trực tiếp ngay trên sân khấu sẽ tạo được ấn tượng về độ tin cậy tốt hơn nhiều so với việc chỉ đi một luồng "Happy Path" hoàn hảo nhưng thiếu chân thực.

## 6. Nếu làm lại

Nếu có thêm thời gian, tôi sẽ tích hợp một công cụ giám sát LLM chuyên dụng (như LangSmith) ngay từ những ngày đầu thay vì chỉ dùng text logging cơ bản. Việc có một dashboard trực quan để toàn đội nhìn thấy ngay prompt nào đang tiêu tốn nhiều token nhất, hay bước gọi tool nào hay bị thất bại, sẽ giúp quá trình debug và tối ưu hóa hệ thống diễn ra nhanh và triệt để hơn rất nhiều.

## 7. AI giúp gì / AI sai gì

- Tác động tích cực: Việc sử dụng AI (như ChatGPT/Gemini) giúp tôi generate nhanh các file cấu hình, script tự động hóa và xử lý các lỗi môi trường lặt vặt. Đồng thời, việc dùng Gamma AI từ prompt text giúp tôi hoàn thiện bộ slide 10 trang chuyên nghiệp chỉ trong tích tắc, giải phóng thời gian để tập trung vào kịch bản nói.
- Hạn chế / Sai lệch: Khi hỏi AI về kiến trúc triển khai, AI thường có xu hướng đề xuất các giải pháp hạ tầng quá phức tạp và "overkill" (như Kubernetes, Terraform, microservices) không hề phù hợp với thời gian và quy mô của một đồ án thực tập prototype. Tôi đã phải tỉnh táo chọn lọc để giữ hệ thống chạy gọn nhẹ trên script và môi trường ảo cơ bản.
