# Individual Reflection — Thái Doãn Minh Hải (2A202600493)

## 1. Role

Phụ trách thiết kế dữ liệu, mock database, viết tools và xây agent.

## 2. Đóng góp cụ thể

- Thiết kế schema dữ liệu cho hệ thống chatbot y tế: thông tin bác sĩ,triệu chứng, lịch hẹn, chuyên khoa, giá khám, giới tính, địa điểm.
- Tạo mock/fake database để demo, bao gồm danh sách bác sĩ, lịch trống, và dữ liệu bệnh nhân mẫu.
- Viết tools để agent có thể tìm bác sĩ theo:
  - triệu chứng
  - địa điểm
  - giá khám
  - giới tính

- Viết tool kiểm tra lịch hẹn của bác sĩ theo ngày/giờ.
- Viết tool đặt lịch, cập nhật trạng thái lịch sau khi người dùng xác nhận.
- Xây agent để tự động quyết định khi nào cần:
  - hỏi thêm thông tin
  - gọi tool tìm bác sĩ
  - kiểm tra lịch
  - đặt lịch

- Test end-to-end nhiều luồng: người dùng chỉ mô tả triệu chứng, người dùng có yêu cầu cụ thể về giá/gần nhà, bác sĩ hết lịch, cần gợi ý thay thế.

## 3. SPEC mạnh/yếu

- Mạnh nhất: flow giữa chatbot và tools khá rõ. Sau khi người dùng mô tả triệu chứng, agent có thể lần lượt suy luận → tìm bác sĩ → kiểm tra lịch → đặt lịch mà không cần hard-code từng case.
- Failure mode mạnh nhất là case “không có bác sĩ phù hợp” hoặc “bác sĩ hết lịch”, vì nhóm đã có mitigation cụ thể: gợi ý bác sĩ khác, lịch gần nhất, hoặc đổi tiêu chí.
- Yếu nhất: mock database còn đơn giản. Dữ liệu mới chỉ có vài bác sĩ và ít lịch hẹn nên chưa phản ánh trường hợp thật như trùng lịch, nhiều chi nhánh, hoặc bác sĩ có nhiều chuyên khoa.
- ROI cũng chưa rõ vì giả định tất cả bệnh nhân đều dùng chatbot thành công. Nếu làm lại nên tách rõ assumption giữa pilot nhỏ và triển khai toàn hệ thống.

## 4. Đóng góp khác

- Hỗ trợ nhóm debug khi agent gọi sai tool hoặc truyền thiếu tham số.
- Viết log để theo dõi agent đang chọn tool nào và vì sao.
- Thêm xử lý fallback khi dữ liệu người dùng chưa đủ, ví dụ chưa nói địa điểm hoặc giới tính bác sĩ mong muốn thì agent sẽ hỏi lại.
- Hỗ trợ test nhiều edge case như:
  - không có bác sĩ đúng giới tính
  - ngân sách quá thấp
  - người dùng chọn giờ đã kín
  - triệu chứng quá chung chung

## 5. Điều học được

Trước hackathon nghĩ AI agent chỉ là “LLM + vài tools”. Sau khi làm mới thấy phần khó nhất là thiết kế dữ liệu và flow giữa các tools.

Nếu dữ liệu không rõ hoặc tool trả về không nhất quán thì agent rất dễ suy luận sai. Ví dụ: tool tìm bác sĩ trả về bác sĩ phù hợp nhưng không có lịch trống, agent sẽ bị kẹt nếu không có bước kiểm tra lịch và fallback.

Cũng học được rằng mock database rất quan trọng. Dù chỉ là dữ liệu giả nhưng nếu thiết kế giống hệ thống thật thì sẽ dễ mở rộng hơn nhiều sau này.

## 6. Nếu làm lại

- Sẽ thiết kế database và format output của tools ngay từ đầu trước khi viết agent.
- Sẽ tạo nhiều dữ liệu fake hơn: nhiều bác sĩ, nhiều ngày, nhiều chi nhánh, nhiều trường hợp conflict.
- Sẽ test integration sớm hơn. Hiện tại nhóm viết tool trước rồi cuối mới nối vào agent nên mất khá nhiều thời gian sửa format dữ liệu.
- Nếu có thêm thời gian sẽ thêm ranking để agent ưu tiên bác sĩ theo nhiều tiêu chí cùng lúc thay vì lọc tuần tự.

## 7. AI giúp gì / AI sai gì

- **Giúp:** dùng ChatGPT và Claude để brainstorm schema dữ liệu, viết nhanh mock database và sinh thêm dữ liệu bác sĩ/lịch hẹn. AI cũng giúp gợi ý cấu trúc tools và flow của agent.
- **Giúp:** dùng AI để debug nhanh khi tool trả sai format hoặc agent không gọi đúng tool.
- **Sai/mislead:** AI từng gợi ý lưu tất cả logic vào prompt thay vì tách thành tools riêng. Ban đầu nghe có vẻ nhanh nhưng sau thử thì prompt rất dài, khó debug, và không xử lý được dữ liệu động như lịch hẹn.
- **Bài học:** AI giúp viết nhanh, nhưng kiến trúc hệ thống và giới hạn scope vẫn phải do mình quyết định.
