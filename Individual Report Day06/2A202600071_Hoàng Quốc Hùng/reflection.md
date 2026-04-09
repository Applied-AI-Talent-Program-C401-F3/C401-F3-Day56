# Reflection - 2A202600071 Hoàng Quốc Hùng

## 1) Role cụ thể trong nhóm
Mình đảm nhận vai trò **Prompt & Spec Integrator**: chịu trách nhiệm thiết kế system prompt lõi, tổng hợp/chuẩn hóa nội dung SPEC cuối, và đại diện nhóm pitching/trao đổi giải pháp với các nhóm khác để lấy phản hồi nhanh.

## 2) Phần phụ trách cụ thể (2-3 đóng góp có output rõ)
1. **Thiết kế `system_prompt.txt` phiên bản dùng cho demo**
   - Output rõ: file prompt hoàn chỉnh với cấu trúc vai trò, giới hạn hành vi, thứ tự xử lý và format trả lời thống nhất.
2. **Biên tập và chốt `spec-final.md`**
   - Output rõ: bản SPEC cuối có đầy đủ mục tiêu, phạm vi, user flow, tiêu chí đánh giá và failure modes để cả nhóm bám theo.
3. **Pitching với các nhóm khác để nhận phản biện chéo**
   - Output rõ: danh sách góp ý nhận được từ các nhóm (về tính khả thi, rủi ro và cách demo), sau đó cập nhật lại các mục tương ứng trong SPEC.

## 3) SPEC phần nào mạnh nhất, phần nào yếu nhất? Vì sao?
- **Mạnh nhất:** phần định nghĩa bài toán + user flow.
  - Vì đã mô tả khá rõ ai là người dùng chính, họ thao tác theo bước nào, và output mong đợi ở mỗi bước nên đội dev và đội demo hiểu cùng một hướng.
- **Yếu nhất:** phần metric định lượng và ngưỡng pass/fail chi tiết.
  - Vì thời gian ngắn, dữ liệu test chưa đủ đa dạng nên một số metric còn ở mức định hướng, chưa đủ chặt để so sánh nhiều phiên bản một cách khách quan.

## 4) Đóng góp cụ thể khác với mục 2
- Thực hiện **test prompt nhanh** theo nhiều kiểu câu hỏi để phát hiện các phản hồi dễ lệch vai trò.
- Hỗ trợ **debug luồng trả lời** khi agent trả output dài nhưng thiếu trọng tâm, đề xuất điều chỉnh instruction order.
- Hỗ trợ nhóm trong việc **đồng bộ thông điệp demo** (cách giải thích chức năng, giới hạn hệ thống, và kịch bản Q&A).

## 5) 1 điều học được trong hackathon mà trước đó chưa biết
Mình học được rằng chất lượng kết quả của agent phụ thuộc rất mạnh vào **thứ tự ưu tiên instruction** trong system prompt, không chỉ phụ thuộc vào nội dung instruction. Chỉ cần đổi thứ tự các ràng buộc quan trọng, hành vi mô hình có thể khác đáng kể.

## 6) Nếu làm lại, đổi gì? (cụ thể)
Nếu làm lại, mình sẽ:
1. Chốt một **bộ test prompt chuẩn (20-30 case)** ngay từ đầu ngày để đo trước/sau mỗi lần sửa prompt.
2. Tách SPEC thành 2 vòng chốt: vòng 1 chốt phạm vi và user story, vòng 2 mới chốt metric để tránh sửa dây chuyền.
3. Gắn mốc thời gian cố định cho phản biện chéo (ví dụ 2 phiên 15 phút) thay vì làm gần cuối.

## 7) AI giúp gì? AI sai/mislead ở đâu?
- **AI giúp:**
  - Tăng tốc brainstorm cấu trúc SPEC và gợi ý khung mục lục hợp lý.
  - Tạo nhanh các biến thể prompt để A/B test và rút ngắn thời gian thử nghiệm.
  - Hỗ trợ viết lại câu chữ pitching gọn, dễ hiểu hơn.
- **AI sai/mislead:**
  - Đôi lúc trả lời quá tự tin với giả định chưa được kiểm chứng (hallucination nhẹ), đặc biệt ở phần đề xuất metric.
  - Một số gợi ý nghe hợp lý nhưng không phù hợp ràng buộc thời gian/dữ liệu thực tế của nhóm.
  - Nếu không kiểm tra lại bằng test case thật, rất dễ bị thuyết phục bởi câu trả lời “mượt” nhưng thiếu độ tin cậy.
