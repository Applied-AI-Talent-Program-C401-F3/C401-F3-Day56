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
