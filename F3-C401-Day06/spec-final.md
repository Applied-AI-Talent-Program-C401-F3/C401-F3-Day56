# Spec Final: AI Doctor Booking - Vinmec

## 1. AI Product Canvas

### Value (Giá trị)
- Với người dùng: Giúp bệnh nhân tìm đúng chuyên khoa và bác sĩ chỉ bằng mô tả triệu chứng tự nhiên, không cần tự đoán chuyên môn y khoa.
- Với bệnh viện: Giảm tải tổng đài, tăng tỷ lệ đặt lịch thành công, tăng trải nghiệm dịch vụ 24/7.
- Kết quả mong đợi: Rút ngắn thời gian từ lúc người dùng bắt đầu hỏi đến lúc xác nhận lịch khám.

### Trust (Niềm tin)
- AI phải minh bạch: đây là trợ lý ảo, không thay thế bác sĩ.
- AI chỉ điều hướng và hỗ trợ đặt lịch, không chẩn đoán bệnh, không kê đơn.
- Có luồng cảnh báo đỏ cho dấu hiệu cấp cứu (ví dụ: đau ngực, khó thở, ngất).

### Feasibility (Tính khả thi)
- Dữ liệu đầu vào khả dụng: danh sách bác sĩ, chuyên khoa, lịch khám trống từ hệ thống bệnh viện (HIS/CRM/API).
- Công nghệ: LLM + RAG cho ánh xạ triệu chứng sang chuyên khoa; function calling để truy vấn lịch khám và đặt lịch.
- Có thể triển khai theo từng giai đoạn: tư vấn chuyên khoa trước, sau đó tối ưu luồng đặt lịch tự động.

### Learning Signal (Tín hiệu học tập)
- Implicit signal: tỷ lệ bỏ ngang từng bước, tỷ lệ hoàn tất đặt lịch.
- Explicit signal: đánh giá hữu ích/không hữu ích sau mỗi phiên.
- Dữ liệu phản hồi được dùng để cải thiện prompt, luật điều hướng và chất lượng gợi ý bác sĩ.

---

## 2. User Stories x 4 Paths

### 2.1. Happy Path (Luồng chuẩn)
- Là người dùng, tôi muốn AI hỏi đủ 4 thông tin bắt buộc: triệu chứng, địa điểm, tầm giá, yêu cầu bác sĩ.
- Là người dùng, tôi muốn nhận danh sách bác sĩ phù hợp kèm lịch trống ngay khi đã đủ thông tin.
- Là hệ thống, tôi muốn gom câu hỏi thông minh để giảm số vòng chat nhưng vẫn đủ dữ liệu.

### 2.2. Bad/Error Path (Luồng sai và lạm dụng)
- Là quản trị viên, tôi muốn AI từ chối các yêu cầu ngoài phạm vi hoặc có dấu hiệu prompt injection/lạm dụng.
- Là kỹ sư tối ưu chi phí, tôi muốn tool tìm bác sĩ chỉ được gọi khi đủ điều kiện và theo thứ tự lọc: Triệu chứng -> Thành phố -> Tầm giá -> Yêu cầu.
- Là người dùng, tôi muốn mọi thông tin bác sĩ đều lấy từ dữ liệu thật của Vinmec, không bịa.

### 2.3. Uncertain Path (Luồng không chắc)
- Là người dùng, nếu mô tả triệu chứng mơ hồ, tôi muốn AI hỏi lại bằng câu gợi ý cụ thể để làm rõ nhu cầu.
- Là hệ thống, tôi muốn giới hạn số vòng hỏi lại (ví dụ tối đa 3 lần) để tránh hội thoại lặp vô hạn.
- Là người dùng, nếu AI vẫn không hiểu sau nhiều lần hỏi, tôi muốn được chuyển sang nhân viên thật.

### 2.4. Lost/Drop Session Path (Mất kết nối)
- Là người dùng, tôi muốn hệ thống nhớ thông tin đã cung cấp khi rớt mạng hoặc đóng app giữa chừng.
- Là hệ thống, tôi muốn lưu state theo thread_id/checkpoint sau mỗi lượt chat.
- Là người dùng, tôi muốn được chào quay lại theo đúng ngữ cảnh dở dang để tiếp tục nhanh.

---

## 3. Eval Metrics + Threshold

### Ưu tiên chiến lược
- Ưu tiên Recall thay vì Precision trong nhận diện ý định y tế, vì bỏ sót ca nguy hiểm (false negative) gây rủi ro cao hơn gợi ý dư chuyên khoa.

### Bộ chỉ số chính
| Metric | Threshold | Red Flag |
|---|---:|---|
| Medical Intent Recall | >= 92% | < 85% |
| Booking Conversion Rate | >= 70% | < 50% |
| Safety Hallucination Rate | < 1% | > 3% |

### Giải thích vận hành
- Medical Intent Recall: phải tìm được ít nhất một chuyên khoa phù hợp cho đa số ca test.
- Booking Conversion Rate: đo khả năng biến tư vấn thành lịch khám thực tế.
- Safety Hallucination Rate: kiểm soát tuyệt đối việc AI tự ý chẩn đoán/kê đơn hoặc bịa thông tin y khoa.

---

## 4. Top 3 Failure Modes

### 4.1. Hallucination thông tin bác sĩ/chuyên môn
- Trigger: AI suy diễn ngoài dữ liệu thật hoặc trả lời khi chưa gọi đúng tool.
- Hậu quả: Người dùng nhận thông tin sai, giảm niềm tin, tăng rủi ro truyền thông.
- Mitigation:
  - Chỉ cho phép trả lời thông tin bác sĩ từ API chính thức.
  - Nếu thiếu dữ liệu thì trả về thông báo không đủ thông tin thay vì đoán.
  - Thiết lập guardrail và kiểm tra nguồn trước khi phản hồi.

### 4.2. Bỏ sót dấu hiệu cấp cứu trong lúc tư vấn
- Trigger: Người dùng mô tả triệu chứng nguy hiểm nhưng AI vẫn đi theo luồng đặt lịch thông thường.
- Hậu quả: Chậm xử lý cấp cứu, rủi ro an toàn nghiêm trọng.
- Mitigation:
  - Rule-based catcher cho từ khóa nguy hiểm chạy song song với LLM.
  - Khi chạm điều kiện đỏ, dừng đặt lịch và chuyển sang cảnh báo cấp cứu + hotline.

### 4.3. Không còn lịch phù hợp hoặc lịch không đồng bộ
- Trigger: Chỉ giữ 1 bác sĩ tốt nhất, không có phương án thay thế; hoặc slot hiển thị còn nhưng thực tế đã bị đặt.
- Hậu quả: Người dùng bỏ quy trình, giảm conversion.
- Mitigation:
  - Luôn chuẩn bị top 3 bác sĩ/slot thay thế.
  - Đồng bộ lịch real-time và tạm giữ slot 2-5 phút khi người dùng xác nhận.
  - Nếu slot vừa hết, gợi ý ngay 3 slot gần nhất khác thay vì báo lỗi chung.

---

## 5. ROI (3 Kịch bản)

| Kịch bản | Giả định chính | Chi phí/tháng | Lợi ích/tháng | Net |
|---|---|---:|---:|---:|
| Conservative | Accuracy ~60%, Adoption 20%, Conversion 10% | 5 triệu | 2 triệu | -3 triệu |
| Realistic | Accuracy ~75%, Adoption 50%, Conversion 20% | 6 triệu | 10 triệu | +4 triệu |
| Optimistic | Accuracy ~90%, Adoption 80%, Conversion 30% | 9 triệu | 30 triệu | +21 triệu |

### Kill Criteria (Điều kiện dừng)
- Cost > Benefit trong 2-3 tháng liên tiếp.
- Conversion < 10% sau khi đã tối ưu.
- Adoption < 20%.
- Accuracy < 60% (mất niềm tin người dùng).

---

## 6. Executive Summary

AI Doctor Booking là trợ lý ảo hỗ trợ người dùng tìm đúng bác sĩ và đặt lịch khám nhanh bằng ngôn ngữ tự nhiên. Trọng tâm của sản phẩm là an toàn y tế, giảm ma sát đặt lịch và tăng hiệu quả vận hành cho bệnh viện.

Giải pháp kết hợp LLM, RAG và function calling để:
- Thu thập đủ thông tin đầu vào (triệu chứng, địa điểm, tầm giá, yêu cầu bác sĩ).
- Gợi ý bác sĩ từ dữ liệu thật, có lịch trống thực tế.
- Kiểm soát rủi ro bằng guardrail, fallback và luồng cảnh báo cấp cứu.

Mục tiêu thành công gồm 3 trụ cột:
- Độ phủ nhận diện ý định y tế cao (Recall).
- Tỷ lệ chuyển đổi đặt lịch tốt (Conversion).
- Tỷ lệ ảo giác y khoa cực thấp (Safety).

Nếu đạt kịch bản Realistic trở lên, hệ thống không chỉ tự cân bằng chi phí mà còn trở thành năng lực cốt lõi giúp Vinmec nâng trải nghiệm chăm sóc và tăng doanh thu bền vững.