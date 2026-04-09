# Vinmec AI Doctor Booking — Prototype

> **Lưu ý:** Đây là sản phẩm prototype phục vụ mục đích thực tập và demo nội bộ.
> Chưa sẵn sàng cho môi trường production.

---

## Giới thiệu

Vinmec AI Doctor Booking là trợ lý ảo hỗ trợ bệnh nhân tìm đúng bác sĩ và đặt lịch khám
chỉ bằng mô tả triệu chứng tự nhiên — không cần tự đoán chuyên khoa.

Hệ thống **không chẩn đoán bệnh**. Nhiệm vụ duy nhất của nó là điều hướng người dùng đến
đúng bác sĩ dựa trên triệu chứng, địa điểm, ngân sách và sở thích cá nhân.

---

## Tính năng chính

- Hỏi và thu thập 4 thông tin đầu vào: triệu chứng, địa điểm, tầm giá, yêu cầu bác sĩ
- Tra cứu bác sĩ phù hợp từ cơ sở dữ liệu thật của Vinmec
- Kiểm tra lịch trống và đặt lịch khám trực tiếp qua hội thoại
- Cảnh báo ngay khi phát hiện triệu chứng cấp cứu (đau ngực, khó thở, v.v.)
- Không bịa thông tin bác sĩ — mọi dữ liệu đều lấy từ `database.json` qua tool call

---

## Kiến trúc hệ thống

```
Người dùng nhập tin nhắn
        │
        ▼
   Agent node
   (GPT-4o-mini + system prompt)
        │
        ├─── gọi tool ──► Tools node
        │                   ├── search_doctors       # Tìm bác sĩ theo triệu chứng
        │                   ├── browse_doctors        # Xem tất cả bác sĩ
        │                   ├── check_availability   # Kiểm tra lịch trống
        │                   └── book_appointment     # Xác nhận đặt lịch
        │                           │
        │◄────── vòng lặp ──────────┘
        │
        └─── trả lời trực tiếp ──► END
```

Công nghệ sử dụng: **LangGraph · LangChain · OpenAI GPT-4o-mini · Python**

---

## Cấu trúc thư mục

```
├── agent.py            # LangGraph graph, agent node, vòng lặp CLI
├── tools.py            # 4 tools: search, browse, check availability, book
├── database.json       # Dữ liệu bác sĩ và bệnh (nguồn duy nhất)
├── system_prompt.txt   # Persona và hướng dẫn hành vi của agent
├── .env                # OPENAI_API_KEY (không commit file này)
└── requirements.txt
```

---

## Cài đặt và chạy thử

### 1. Cài dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình API key

```bash
cp .env.example .env
# Mở file .env và điền OPENAI_API_KEY của bạn
```

### 3. Chạy agent

```bash
python agent.py
```

Gõ `quit` hoặc `exit` để thoát khỏi vòng lặp chat.

---

## Luồng hội thoại

Hệ thống xử lý 2 trường hợp chính:

**Có triệu chứng** → `search_doctors` → gợi ý bác sĩ → kiểm tra lịch → đặt lịch

**Không có triệu chứng** (tái khám, khám tổng quát) → `browse_doctors` → lọc theo sở thích → đặt lịch

Nếu mô tả triệu chứng mơ hồ, agent hỏi lại tối đa 3 lần trước khi chuyển sang
nhân viên hỗ trợ thật.

---

## Quyết định thiết kế quan trọng

| Quyết định | Lý do |
|---|---|
| Ưu tiên Recall hơn Precision | Bỏ sót ca nguy hiểm rủi ro hơn gợi ý dư chuyên khoa |
| Không trả lời ngoài database | Tránh hallucination thông tin y tế |
| Rule-based catcher cho cấp cứu | Chạy song song LLM, không phụ thuộc vào LLM phán đoán |
| Giới hạn 10 messages trong context | Kiểm soát chi phí token |
| System prompt chỉ inject 1 lần | Tránh token trùng lặp qua nhiều lượt |

---

## Chỉ số đánh giá (Eval Targets)

| Chỉ số | Mục tiêu | Ngưỡng dừng |
|---|---:|---:|
| Medical Intent Recall | ≥ 92% | < 85% |
| Booking Conversion Rate | ≥ 70% | < 50% |
| Safety Hallucination Rate | < 1% | > 3% |

---

## Top 3 rủi ro và biện pháp xử lý

**1. Hallucination thông tin bác sĩ**
Agent chỉ được phép trả về thông tin từ kết quả tool. Nếu không có kết quả,
trả về thông báo rõ ràng thay vì tự điền.

**2. Bỏ sót triệu chứng cấp cứu**
Rule-based keyword catcher chạy song song với LLM. Khi phát hiện từ khóa nguy hiểm,
dừng luồng đặt lịch và hiển thị cảnh báo + hotline cấp cứu ngay lập tức.

**3. Lịch khám không đồng bộ hoặc hết slot**
Luôn chuẩn bị top 3 bác sĩ/slot thay thế. Khi slot vừa hết, gợi ý ngay 3 slot
gần nhất thay vì báo lỗi chung chung.

---

## Phân công nhóm

| Vai trò | Thành viên |
|---|---|
| Architect Engineer | Khương Hải Lâm |
| LLM / Prompt Engineer | Hoàng Quốc Hùng |
| Database Engineer | Thái Doãn Minh Hải |
| Frontend & UI / Integration | Đặng Tuấn Anh |
| Tool Engineer & Evaluation | Lương Trung Kiên |
| DevOps & Presentation | Lưu Lê Gia Bảo |

> **Ghi chú:** Phần code triển khai các tool (`tools.py`) là đóng góp chung của cả nhóm,
> không thuộc trách nhiệm riêng của bất kỳ thành viên nào. Các thành viên cũng đồng thời góp ý cách cải tiến prompt system và bộ tool.

### Mô tả chi tiết từng vai trò

**Khương Hải Lâm — Architect Engineer**
Chịu trách nhiệm thiết kế kiến trúc tổng thể của hệ thống, xác định độ ưu tiên tính năng,
định nghĩa tiêu chí chấp nhận (acceptance criteria) và theo dõi kill criteria. Phối hợp
giữa các vai trò trong nhóm và đảm bảo mục tiêu sản phẩm nhất quán xuyên suốt quá trình
phát triển.

**Hoàng Quốc Hùng — LLM / Prompt Engineer**
Viết và cải tiến `system_prompt.txt`. Thiết kế luồng hội thoại: cách agent hỏi đủ
4 thông tin bắt buộc, xử lý triệu chứng mơ hồ, giới hạn vòng hỏi lại (tối đa 3 lần),
phát hiện và từ chối prompt injection. Chịu trách nhiệm về chất lượng ngôn ngữ và
trải nghiệm hội thoại.

**Thái Doãn Minh Hải — Database Engineer**
Xây dựng và sở hữu `database.json`, thiết kế kết cấu dữ liệu và logic ánh xạ triệu
chứng → bệnh → chuyên khoa, sinh slot lịch khám và các hàm normalize dữ liệu.
Đảm bảo không có thông tin nào được trả về ngoài database, duy trì tính toàn vẹn
của dữ liệu và kiểm soát chất lượng output của model khi sử dụng bộ dữ liệu này.

**Đặng Tuấn Anh — Frontend & UI / Integration**
Tích hợp agent vào giao diện chat (web hoặc mobile). Xử lý session persistence
theo `thread_id`, luồng kết nối lại khi mất mạng và tin nhắn chào quay lại
theo đúng ngữ cảnh. Chịu trách nhiệm UX cho card bác sĩ, chọn slot và màn hình
xác nhận đặt lịch. Đồng thời tối ưu hóa prompt để Chatbot hoạt động đúng ngữ cảnh khi đưa vào môi trường test thực tế

**Lương Trung Kiên — Tool Engineer & Evaluation**
Thiết kế đặc tả và cấu trúc cho bộ tool mà agent sử dụng, dựa trên spec sản phẩm
và database hiện có. Giám sát việc triển khai để đảm bảo các tool hoạt động đúng
theo thiết kế. Xây dựng bộ test case cho cả 4 luồng (happy path, error path,
uncertain path, lost session path), đo lường 3 chỉ số chính, duy trì bộ test
từ khóa cấp cứu và chạy regression test mỗi khi prompt hoặc tool logic thay đổi.

**Lưu Lê Gia Bảo — DevOps & Presentation**
Quản lý môi trường, secrets trong `.env`, dependency và CI pipeline. Xây dựng
chiến lược đồng bộ lịch real-time (mock hoặc HIS API stub cho prototype). Thiết
lập logging để theo dõi tỷ lệ drop-off từng bước và conversion rate, đồng thời
giám sát chi phí token mỗi phiên. Phụ trách chuẩn bị và trình bày sản phẩm.

---

## Giới hạn của prototype này

- Dữ liệu bác sĩ là mock, không kết nối HIS/CRM thật của Vinmec
- Slot lịch khám được sinh tự động, không đồng bộ real-time
- Chưa có xác thực danh tính bệnh nhân
- Chưa tích hợp thanh toán
- Giao diện hiện tại chỉ là CLI

---

*Prototype này được phát triển trong khuôn khổ chương trình thực tập.
Mọi thông tin bác sĩ và dữ liệu y tế trong `database.json` chỉ mang tính minh họa.*
