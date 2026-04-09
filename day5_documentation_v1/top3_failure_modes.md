# Failure Mode 3: Không còn lịch của bác sĩ phù hợp

## 1. Không còn lịch của bác sĩ phù hợp nhưng không gợi ý bác sĩ thay thế

### Trigger

- Chatbot chỉ lưu 1 bác sĩ “tốt nhất”.
- Khi bác sĩ đó hết lịch, hệ thống không tìm thêm bác sĩ khác cùng chuyên khoa.
- Ví dụ: bệnh nhân cần khám Tim mạch, bác sĩ A hết lịch nên chatbot trả về “Không còn lịch”.

### Hậu quả

- Người dùng dừng luôn quá trình đặt lịch.
- Tăng tỉ lệ abandon sau bước xem lịch.
- Bệnh viện mất lượt khám dù vẫn còn bác sĩ B, C phù hợp.

### Mitigation

- Luôn chuẩn bị top 3 bác sĩ cho mỗi trường hợp.
- Nếu bác sĩ A hết lịch:
  - Gợi ý bác sĩ B cùng chuyên khoa.
  - Gợi ý bác sĩ C có kinh nghiệm tương tự.

Ví dụ hiển thị:

```text
Bác sĩ A: hết lịch
Bác sĩ B: còn 15:00 hôm nay
Bác sĩ C: còn 09:00 ngày mai
```

---

## 2. Không còn lịch gần, chỉ còn lịch quá xa

### Trigger

- Bác sĩ phù hợp chỉ còn lịch sau 7–14 ngày.
- Chatbot vẫn hiển thị đúng bác sĩ đó mà không đề xuất thời gian gần hơn.
- Người bệnh cần khám sớm nhưng thấy lịch quá xa.

### Hậu quả

- Người dùng cảm thấy chờ quá lâu và bỏ cuộc.
- Chuyển sang bệnh viện khác.
- Giảm tỉ lệ booking completion.

### Mitigation

- Nếu lịch của bác sĩ chính > 3 ngày:
  - Tự động hiển thị:
    - Bác sĩ khác cùng chuyên khoa có lịch sớm hơn.
    - Khám online.
    - Cơ sở khác của cùng bệnh viện.

Ví dụ:

```text
Bác sĩ A: còn lịch sau 10 ngày
Bác sĩ B: còn lịch 16:00 hôm nay
Bác sĩ C: còn lịch sáng mai
Khám online với bác sĩ A: tối nay 20:00
```

---

## 3. Lịch hiển thị còn trống nhưng thực tế đã bị người khác đặt

### Trigger

- Lịch khám không được đồng bộ real-time.
- Hai người cùng chọn một khung giờ.
- Người thứ hai bấm đặt nhưng slot đã bị người khác lấy.

### Hậu quả

- Người dùng thấy hệ thống “báo sai”.
- Mất niềm tin vào chatbot và bệnh viện.
- Người dùng phải chọn lại từ đầu.

### Mitigation

- Đồng bộ lịch theo thời gian thực từ hệ thống HIS/CRM.
- Khi người dùng chọn slot:
  - Tạm giữ slot trong 2–5 phút.
  - Sau đó mới xác nhận thanh toán/đặt lịch.

- Nếu slot vừa hết:
  - Không báo lỗi chung chung.
  - Ngay lập tức hiển thị 3 slot gần nhất khác.

Ví dụ:

```text
Khung giờ 14:00 vừa được đặt.
Bạn có thể chọn 14:30, 15:00 hoặc 16:00.
```
