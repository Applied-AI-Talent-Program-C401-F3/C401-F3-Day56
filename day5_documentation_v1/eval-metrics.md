# Eval Metrics + Threshold: AI Doctor Booking

## Ưu tiên Precision hay Recall?

- [x] **Recall** — tìm được hết những cái cần tìm (ít false negative)
- [ ] **Precision** — khi AI nói "có" thì thực sự đúng (ít false positive)

### Tại sao chọn Recall?

Trong y tế, **Safety First (An toàn là trên hết)**. Nếu khách hàng có triệu chứng nguy hiểm mà AI không nhận diện được (**False Negative**) để điều trị kịp thời thì hậu quả cực kỳ nghiêm trọng.

Thà gợi ý "nhầm" thêm một chuyên khoa để kiểm tra (**False Positive**) còn hơn là bỏ sót bệnh lý của bệnh nhân.

### Nếu ưu tiên ngược lại (Precision) thì sao?

Nếu chỉ ưu tiên Precision (chỉ gợi ý khi chắc chắn gần như 100%), AI sẽ trở nên quá thận trọng và thường xuyên trả lời "Tôi không biết", dẫn đến việc bệnh nhân bị bỏ sót các dấu hiệu bệnh lý quan trọng, làm mất đi ý nghĩa của một trợ lý y tế thông minh.

## Metrics Table

| Metric | Threshold | Red flag (dừng khi) |
|---|---:|---|
| Medical Intent Recall (Tỉ lệ nhận diện đúng triệu chứng) | >= 92% | < 85% -> AI bỏ sót quá nhiều dấu hiệu bệnh lý |
| Booking Conversion Rate (Tỉ lệ đặt lịch thành công) | >= 70% | < 50% -> Luồng tư vấn quá phức tạp, khách bỏ cuộc |
| Safety Hallucination Rate (Tỉ lệ bịa đặt thông tin y khoa) | < 1% | > 3% -> AI tư vấn sai kiến thức y khoa căn bản |

## Chi tiết các chỉ số cho Hackathon

### 1. Medical Intent Recall (Độ phủ nhận diện chuyên khoa)

**Tại sao chọn Recall?**

Việc gợi ý nhầm bác sĩ Da liễu cho một người đau cơ (sai Precision) chỉ gây tốn thời gian. Nhưng nếu người dùng nói "đau ngực" mà AI không gợi ý bác sĩ Tim mạch (sai Recall) thì đó là một rủi ro tính mạng.

**Ngưỡng đạt:** >= 92% các ca test phải tìm ra được ít nhất một chuyên khoa liên quan.

**Red flag:** Khi hệ thống liên tục trả lời "Bạn hãy mô tả thêm" đối với các triệu chứng đã rõ ràng, hoặc bỏ sót các từ khóa cấp cứu (đau thắt, khó thở, hôn mê).

### 2. Booking Success Rate (Hiệu quả chuyển đổi)

**Tại sao quan trọng?**

Hackathon rất coi trọng việc sản phẩm có dùng được không. Nếu AI tư vấn hay nhưng người dùng không thể chốt được lịch khám, ứng dụng sẽ thất bại.

**Ngưỡng đạt:** >= 70% người dùng sau khi nhận gợi ý sẽ thực hiện thao tác chọn giờ và xác nhận đặt lịch.

**Red flag:** Tỉ lệ thoát (Drop-off) ở bước chọn bác sĩ quá cao (> 50%), chứng tỏ AI gợi ý bác sĩ không phù hợp hoặc không đủ tin cậy.

### 3. Safety Hallucination Rate (Kiểm soát "vị thuốc giả")

**Tại sao quan trọng?**

AI y tế tuyệt đối không được tự ý kê đơn hoặc khẳng định bệnh (diagnosis) nếu không có dữ liệu. Nó chỉ được đóng vai trò "điều hướng" (triage).

**Ngưỡng đạt:** < 1%. AI chỉ được phép đưa ra các lời khuyên mang tính thủ tục hoặc định hướng chuyên khoa.

**Red flag:** AI tự ý khuyên bệnh nhân mua thuốc cụ thể (ví dụ: "Bạn hãy uống kháng sinh X đi") hoặc khẳng định chắc chắn "Bạn bị bệnh Y rồi". Đây là lỗi nghiêm trọng nhất trong y tế AI.
