# AI Product Canvas: AI Doctor Booking Chatbot

**Dự án:** Trợ lý ảo AI tìm & đặt lịch khám bệnh (Track B - Vinmec)
**Mục tiêu:** Giúp bệnh nhân tìm đúng bác sĩ/chuyên khoa dựa trên triệu chứng bằng ngôn ngữ tự nhiên và hoàn tất đặt lịch nhanh chóng.

---

## 1. Value (Giá trị mang lại)

**Đối với Bệnh nhân (Users):**
* **Giảm ma sát (Frictionless):** Không cần phải có kiến thức y khoa để biết mình cần khám chuyên khoa nào.
* **Tiện lợi 24/7:** Hỗ trợ đặt lịch bất kể ngày đêm mà không cần chờ đợi tổng đài.
* > *Ví dụ cụ thể:* Bệnh nhân bị "đau bụng dưới, buồn nôn". Thay vì phải tự mò mẫm xem nên chọn Khoa Tiêu hóa hay Sản phụ khoa, bệnh nhân chỉ cần chat triệu chứng. AI sẽ hỏi thêm 1-2 câu để khoanh vùng và lập tức đưa ra danh sách bác sĩ phù hợp kèm lịch trống.

**Đối với Bệnh viện (Business/Vinmec):**
* **Tăng tỉ lệ chuyển đổi (Conversion Rate):** Bệnh nhân dễ tìm đúng bác sĩ -> Tỉ lệ chốt lịch khám (Booking) cao hơn.
* **Tối ưu nguồn lực:** Giảm tải cho đội ngũ trực tổng đài (Call center) trong việc tư vấn phân loại bệnh cơ bản (Triage).
* > *Ví dụ cụ thể:* Vào giờ cao điểm (thứ 2 đầu tuần), AI có thể xử lý đồng thời hàng ngàn lượt chat hỏi lịch khám, giúp tổng đài viên tập trung giải quyết các ca cấp cứu hoặc khiếu nại phức tạp.

---

## 2. Trust (Niềm tin & An toàn)

Trong y tế, sự tin tưởng và an toàn là yếu tố sống còn (giống như việc bạn đã chọn ưu tiên *Recall* trong Eval Metrics).

* **Minh bạch danh tính (Transparency):** Khẳng định rõ ràng đây là AI, không phải bác sĩ.
* **Không chẩn đoán, chỉ điều hướng (Triage, no Diagnosis):** Tuyệt đối không kết luận bệnh hoặc kê đơn thuốc (để kiểm soát Safety Hallucination Rate < 1%).
* **Luồng xử lý khẩn cấp (Emergency Fallback):** Tự động nhận diện các từ khóa nguy hiểm và kích hoạt cảnh báo đỏ.
* > *Ví dụ cụ thể:* Ngay khi người dùng chat: "Tôi đang rất khó thở và đau nhói ở ngực", AI sẽ **dừng ngay lập tức** việc hỏi han đặt lịch và hiển thị thông báo đỏ: *"Cảnh báo: Triệu chứng của bạn có thể là dấu hiệu cấp cứu y tế. Xin đừng chờ đợi. Vui lòng gọi ngay 115 hoặc đến phòng cấp cứu gần nhất!"*, kèm theo nút bấm gọi hotline cấp cứu của Vinmec.

---

## 3. Feasibility (Tính khả thi về mặt kỹ thuật & Dữ liệu)

* **Nguồn dữ liệu (Data Sources):** * Hệ thống thông tin bệnh viện (HIS) để lấy Real-time API về danh sách bác sĩ, chuyên khoa, và giờ khám trống.
    * Tài liệu y khoa cơ bản của bệnh viện (Cẩm nang triệu chứng - chuyên khoa) để làm knowledge base cho AI.
* **Công nghệ (Tech Stack):** * Sử dụng LLM (VD: Gemini/GPT) kết hợp RAG (Retrieval-Augmented Generation) để mapping (nối) triệu chứng của user với chuyên khoa.
    * Sử dụng Function Calling (Tool use) để gọi API đặt lịch thực tế.
* > *Ví dụ cụ thể:* Khi AI xác định bệnh nhân cần khám "Da liễu", hệ thống sẽ dùng Function Calling gọi một API nội bộ dạng `get_available_doctors(specialty="dermatology", date="today")` để kéo thông tin lịch trống của bác sĩ đưa vào khung chat, rất khả thi và không cần xây dựng lại hệ thống booking từ đầu.

---

## 4. Learning Signal (Tín hiệu học tập để cải tiến AI)

Làm sao để biết AI đang làm tốt và làm sao để nó thông minh hơn mỗi ngày?

* **Implicit Signals (Tín hiệu ngầm/Hành vi):** * Tỉ lệ Drop-off (Người dùng thoát ngang ở bước nào?).
    * Tỉ lệ Booking Success Rate (đã định nghĩa >= 70% trong Eval Metrics).
* **Explicit Signals (Tín hiệu chủ động/Phản hồi):** * Đánh giá trực tiếp của người dùng sau mỗi lượt tư vấn.
* > *Ví dụ cụ thể:* Sau khi AI gợi ý: *"Dựa trên triệu chứng, bạn nên khám chuyên khoa Nội Thần Kinh cùng Bác sĩ A"*, dưới tin nhắn sẽ có 2 nút [👍 Hữu ích] và [👎 Không liên quan]. Nếu người dùng bấm 👎 và sau đó tự thoát ra tìm thủ công bác sĩ "Khoa Cơ xương khớp", hệ thống sẽ lưu lại log này (Triệu chứng X - Sai lầm: Nội Thần Kinh - Thực tế chọn: Cơ xương khớp) để đội ngũ dev đánh giá và tinh chỉnh lại (fine-tune) prompt hoặc RAG database cho chính xác hơn.

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
