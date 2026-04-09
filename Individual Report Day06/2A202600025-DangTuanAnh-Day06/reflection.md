# Individual reflection — Đặng Tuấn Anh (2A202600025)

## 1. Role
UI/UX designer + prompt engineer. Đảm nhiệm chính việc thiết kế trải nghiệm người dùng (conversation flow) cho chatbot và trực tiếp viết/tối ưu hóa system prompt để điều hướng AI hoạt động đúng kịch bản y tế.

## 2. Đóng góp cụ thể
Về UX/UI: Thiết kế luồng hội thoại (conversation flow) tối ưu trải nghiệm người dùng, gồm 5 bước logic giúp thu thập thông tin hiệu quả mà không làm bệnh nhân bối rối: Hỏi vị trí đau → Thời gian → Mức độ → Tiền sử → Đưa ra gợi ý. Xây dựng layout cho poster demo dự án, đảm bảo truyền tải rõ ràng thông điệp sản phẩm.

Về Prompt Engineering: Trực tiếp viết, tinh chỉnh và kiểm thử 3 phiên bản system prompt. Đưa ra quyết định chốt phiên bản v3 dựa trên tỷ lệ Recall tốt nhất qua quá trình đánh giá 10 test cases thực tế.

## 3. SPEC mạnh/yếu
- Điểm mạnh nhất (Failure Modes): Nhóm đã phân tích sâu các rủi ro, điển hình là case "triệu chứng chung chung" khiến AI đưa ra gợi ý quá rộng. Đã đề xuất phương án giảm thiểu (mitigation) hiệu quả về mặt UX: thiết kế để AI chủ động hỏi thêm các câu follow-up nhằm thu hẹp phạm vi thay vì bắt người dùng tự đoán.

- Điểm yếu nhất (ROI): Ba kịch bản tài chính hiện tại có giả định khá giống nhau, chỉ khác biệt ở số lượng người dùng. Cần tách biệt rõ ràng các giả định. (Ví dụ: Kịch bản Thận trọng (Conservative) có thể là chỉ áp dụng thử nghiệm chatbot tại 1 chi nhánh để đo lường; trong khi Kịch bản Lạc quan (Optimistic) là rollout toàn hệ thống bệnh viện kết hợp với chiến dịch truyền thông lớn).

## 4. Đóng góp khác
- Chủ động test prompt với 10 loại triệu chứng khác nhau và ghi chép log kết quả chi tiết vào file prompt-tests.md để toàn đội tiện theo dõi.

- Hỗ trợ thành viên Lâm debug các chỉ số đánh giá (eval metrics). Cụ thể, thay vì dùng một chỉ số "Accuracy" chung chung, tôi đã đề xuất tách riêng độ chính xác (Precision) cho từng chuyên khoa để đánh giá sát sao và thực tế hơn.

## 5. Điều học được
Trước hackathon, tôi luôn nghĩ Precision và Recall chỉ là các chỉ số đo lường kỹ thuật thuần túy. Sau khi trực tiếp thiết kế AI triage (phân loại bệnh nhân), tôi nhận ra đây thực chất là những quyết định về mặt sản phẩm (Product Decisions), không chỉ là Engineering Decisions.
(Ví dụ thực tế: Đối với Khoa Cấp cứu, tôi phải thiết kế để chatbot ưu tiên Recall cao — thà báo động nhầm (false alarm) còn hơn bỏ sót bệnh nhân nguy kịch. Ngược lại, đối với các Khoa Chuyên sâu, cần ưu tiên Precision — vì nếu chatbot phân tích sai chuyên khoa, sẽ làm lãng phí thời gian chờ đợi và gây tâm lý ức chế cho bệnh nhân).

## 6. Nếu làm lại
Tôi sẽ phân bổ thời gian để kiểm thử (test) prompt sớm hơn. Trong thực tế, ngày đầu tiên tôi chỉ tập trung viết tài liệu SPEC, mãi đến trưa ngày D6 mới bắt đầu test prompt. Nếu bắt đầu quy trình test ngay từ tối ngày D5, tôi có thể lặp lại (iterate) thêm 2-3 vòng kiểm thử sớm. Trải nghiệm UX của chatbot lúc đó chắc chắn sẽ mượt mà và tự nhiên hơn nhiều.

## 7. AI giúp gì / AI sai gì
- Tác động tích cực: Sử dụng Claude để brainstorm các "failure modes" rất hiệu quả — AI đã phát hiện ra trường hợp "tương tác thuốc" (drug interaction), một rủi ro cực kỳ quan trọng mà nhóm chưa nghĩ tới. Đồng thời, việc dùng Gemini thông qua AI Studio giúp luân chuyển và test prompt diễn ra rất nhanh.

- Hạn chế / Sai lệch: Claude có xu hướng liên tục gợi ý thêm tính năng, điển hình là tính năng "đặt lịch khám trực tiếp thông qua chatbot". Dù xét về UX thì tính năng này rất liền mạch, nhưng scope (phạm vi) lại quá khổng lồ so với thời lượng một cuộc thi hackathon. Nhờ phát hiện kịp thời, tôi đã gạt bỏ tính năng này để tránh bẫy "scope creep" (phình to dự án).

- Kết luận: AI là trợ lý brainstorm xuất sắc để mở rộng ý tưởng, nhưng người thiết kế phải là người đưa ra quyết định để vạch ra ranh giới scope cuối cùng.