# Mini AI Spec: Vinmec AI Care Assistant (Trợ lý ảo Hậu phẫu & Chăm sóc cá nhân)

**Vấn đề:** Bệnh nhân sau khi xuất viện/khám bệnh thường có nhiều thắc mắc về đơn thuốc, dinh dưỡng hoặc triệu chứng phụ. Gọi tổng đài thì mất thời gian chờ đợi, tự tra Google thì thông tin y khoa không đáng tin cậy.

**Giải pháp:** Tích hợp AI (RAG + LLM) vào ứng dụng MyVinmec. AI sẽ truy xuất trực tiếp từ hồ sơ bệnh án của bệnh nhân và cẩm nang y khoa chuẩn của Vinmec để giải đáp, theo dõi và tự động cảnh báo bác sĩ nếu có triệu chứng nguy hiểm.

---

## 1. AI Product Canvas

- **Value (Giá trị):** Giảm tải cho tổng đài chăm sóc khách hàng, tăng sự an tâm cho bệnh nhân với hỗ trợ 24/7, phát hiện sớm các biến chứng hậu phẫu.
- **Trust (Niềm tin):** Dữ liệu được trích xuất (RAG) 100% từ tài liệu chuyên môn của Vinmec và bệnh án cá nhân. Luôn có Disclaimer: _"AI chỉ hỗ trợ cung cấp thông tin, không thay thế chẩn đoán của bác sĩ"_.
- **Feasibility (Tính khả thi):** Dữ liệu hồ sơ bệnh án điện tử (EMR) và cẩm nang y tế đã có sẵn. Có thể sử dụng các giải pháp Private LLM/Cloud tuân thủ chuẩn bảo mật y tế (HIPAA).
- **Learning Signal (Tín hiệu học tập):** Nút đánh giá (Hữu ích/Không hữu ích) từ bệnh nhân; Tỷ lệ AI chuyển tuyến (escalate) thành công cho bác sĩ trực.

---

## 2. User Stories x 4 paths

- **Happy Path:** Bệnh nhân hỏi: _"Tôi vừa mổ ruột thừa hôm qua, ăn cháo thịt băm được không?"_. AI hiểu ngữ cảnh (bệnh nhân mổ ruột thừa), truy xuất cẩm nang dinh dưỡng của Vinmec và đáp: _"Chào bạn, bạn có thể ăn cháo thịt băm nhưng cần nấu loãng, ăn thành nhiều bữa nhỏ..."_
- **Low-confidence Path:** Bệnh nhân hỏi: _"Tôi thấy hơi đau ở bụng"_. AI không đủ tự tin để chẩn đoán mức độ. AI phản hồi bằng cách hỏi đào sâu: _"Bạn đau ở quanh vết mổ hay vị trí khác? Đau âm ỉ hay quặn từng cơn?"_. Sau đó thu thập thông tin và chuyển đoạn chat cho y tá trực.
- **Failure Path:** Bệnh nhân dùng từ ngữ địa phương/từ lóng quá phức tạp hoặc gửi ảnh mờ AI không đọc được. AI phản hồi: _"Xin lỗi, tôi chưa hiểu rõ tình trạng của bạn. Để đảm bảo an toàn, vui lòng nhấn nút [GỌI HOTLINE] để gặp trực tiếp tổng đài viên Vinmec."_
- **Correction Path:** AI nhắc uống thuốc nhưng bệnh nhân phản hồi: _"Bác sĩ bảo tôi ngừng loại thuốc này rồi"_. AI ngay lập tức xin lỗi, ghi nhận sự thay đổi, hướng dẫn bệnh nhân làm theo lời bác sĩ, đồng thời tạo một _ticket_ ẩn gửi đến hệ thống để bác sĩ kiểm tra lại việc cập nhật bệnh án (EMR).

---

## 3. Eval Metrics

- **Metric 1: Task Completion Rate** (Tỷ lệ giải quyết trọn vẹn câu hỏi FAQ/hướng dẫn mà không cần can thiệp của con người) > **60%**.
- **Metric 2: Medical RAG Accuracy** (Độ chính xác của kiến thức y khoa được truy xuất) > **98%**.
- **Metric 3: Response & Triage Latency** (Thời gian phản hồi và phân loại ca bệnh) < **3 giây**.
- 🔴 **Red Flag:** Tỷ lệ _False Negative_ cho các ca cấp cứu > 0%. (Tuyệt đối không được phép xảy ra trường hợp: bệnh nhân có dấu hiệu nguy kịch như khó thở, tức ngực nhưng AI lại khuyên "nghỉ ngơi tại nhà").

---

## 4. Top 3 Failure Modes

### 4.1. Hallucination (Ảo giác y khoa bịa đặt kiến thức)

- **Trigger:** Bệnh nhân hỏi một bệnh lý nằm ngoài dữ liệu của Vinmec.
- **Hậu quả:** Bệnh nhân làm theo lời khuyên sai, gây hại sức khỏe, Vinmec khủng hoảng truyền thông.
- **Mitigation:** System prompt cực kỳ khắt khe, chỉnh `Temperature = 0`. Nếu không tìm thấy trong RAG, ép buộc AI trả lời _"Tôi không có chuyên môn về vấn đề này, vui lòng hỏi bác sĩ"_.

### 4.2. Bỏ sót tín hiệu cấp cứu (Triage Failure)

- **Trigger:** Bệnh nhân mô tả triệu chứng nhẹ nhàng (ví dụ: "thấy mệt mệt, đổ mồ hôi lạnh") nhưng thực chất là dấu hiệu nhồi máu cơ tim.
- **Hậu quả:** Trễ thời gian "vàng" cấp cứu.
- **Mitigation:** Cài đặt thêm một lớp Rule-based Keyword Catcher (bắt từ khóa y tế nguy hiểm) chạy song song với LLM. Có từ khóa nguy hiểm là lập tức kích hoạt luồng cảnh báo đỏ.

### 4.3. Vi phạm quyền riêng tư dữ liệu chéo (Data Leakage)

- **Trigger:** Lỗi truy xuất vector database, bệnh nhân A hỏi nhưng AI lại trả về một phần thông tin bệnh án của bệnh nhân B.
- **Hậu quả:** Vi phạm nghiêm trọng luật bảo mật thông tin y tế.
- **Mitigation:** Cấu hình Metadata Filtering chặt chẽ: Query của User ID nào chỉ được phép vector-search trong bộ tài liệu được gắn tag ID đó và bộ tài liệu Public.

---

## 5. ROI (3 Kịch bản)

- **Conservative (Thận trọng - Đạt yêu cầu cơ bản):** Giảm 15% khối lượng công việc trả lời câu hỏi lặp lại (FAQ) cho tổng đài. Tỷ lệ hài lòng của khách hàng tăng nhẹ. Thời gian hòa vốn ước tính: 1.5 năm.
- **Realistic (Thực tế - Kỳ vọng):** Giảm 35% chi phí vận hành đội ngũ chăm sóc sau khám. Thông qua việc giải đáp kịp thời, giảm 10% các ca tái khám không cần thiết. Hệ thống AI tự động gợi ý lịch tái khám đúng hạn (Upsell dịch vụ), tăng doanh thu nhẹ.
- **Optimistic (Lạc quan - Đột phá):** Tính năng trở thành điểm sáng (Killer-feature) của MyVinmec. Trải nghiệm "chăm sóc như bác sĩ riêng" giúp Vinmec thu hút thêm 15% khách hàng mới từ các viện tư nhân khác. Thời gian hòa vốn < 6 tháng.

---

## 6. Tổng hợp Mini AI Spec (Executive Summary)

> **Dự án: Vinmec AI Care Assistant**
>
> Định vị là một trợ lý ảo y tế hậu phẫu tích hợp trên MyVinmec, sử dụng kiến trúc RAG để truy vấn cẩm nang y tế và EMR. Mục tiêu cốt lõi là tối ưu hóa **trải nghiệm bệnh nhân (Patient Experience)**, giữ kết nối 24/7 sau khi bệnh nhân rời khỏi bệnh viện, giải quyết "nút thắt cổ chai" của tổng đài CSKH và tạo ra lớp phòng vệ đầu tiên (Triage) cảnh báo các biến chứng y khoa.
>
> Sản phẩm nhấn mạnh vào tính **An toàn (Safety)** thông qua hệ thống Fallback thông minh: Mọi câu hỏi ngoài vùng dữ liệu (Out-of-domain) hoặc có từ khóa nguy hiểm đều được định tuyến (escalate) ngay lập tức tới bác sĩ trực. Việc triển khai thành công không chỉ tiết kiệm >30% chi phí vận hành tổng đài mà còn biến dịch vụ hậu mãi của Vinmec trở thành chuẩn mực mới trong ngành y tế tư nhân, đem lại ROI thực tế qua việc tối ưu hóa nhân sự và giữ chân khách hàng (Retention).
