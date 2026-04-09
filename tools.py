# Revised Tools Based on `database.json`
from langchain_core.tools import tool
import json
import re
import unicodedata
from datetime import datetime, timedelta

# ============================================================================
# LOAD DATA
# ============================================================================

def load_data_from_json():
    with open("database.json", "r", encoding="utf-8") as f:
        return json.load(f)


DATA = load_data_from_json()
DISEASES_DB = DATA["DISEASES_DB"]
DOCTORS_RAW = DATA["DOCTORS_DB"]
DAY_MAPPING = DATA["DAY_MAPPING"]


# ============================================================================
# HELPERS
# ============================================================================

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def normalize_gender(gender: str) -> str:
    mapping = {
        "male": "nam",
        "female": "nữ",
        "nam": "nam",
        "nu": "nữ",
        "nữ": "nữ",
    }
    return mapping.get(gender.strip().lower(), "")


def normalize_specialty(specialty: str) -> str:
    specialty = specialty.strip().lower()

    aliases = {
        "nội khoa": "nội tổng quát",
        "nội tổng quát": "nội tổng quát",
        "tim mạch": "tim mạch",
        "tai mũi họng": "tai mũi họng",
        "da liễu": "da liễu",
        "hô hấp": "hô hấp",
        "tiêu hóa": "tiêu hóa",
        "thần kinh": "thần kinh",
        "nội tiết": "nội tiết",
        "tiết niệu": "tiết niệu",
        "cơ xương khớp": "cơ xương khớp",
    }

    return aliases.get(specialty, specialty)


def symptom_matches(text: str, symptom_keyword: str) -> bool:
    text = text.lower()
    symptom_keyword = symptom_keyword.lower()

    pattern = rf"(?<!\w){re.escape(symptom_keyword)}(?!\w)"
    return re.search(pattern, text) is not None


def generate_available_slots(working_days, time_range, days_ahead=14):
    slots = []

    start_hour = int(time_range.split("-")[0].split(":")[0])
    end_hour = int(time_range.split("-")[1].split(":")[0])

    today = datetime.now()

    for i in range(days_ahead):
        day = today + timedelta(days=i)

        weekday = day.isoweekday()  # Monday=1 ... Sunday=7
        if weekday not in working_days:
            continue

        for hour in range(start_hour, end_hour):
            slot = day.replace(hour=hour, minute=0, second=0, microsecond=0)
            slots.append(slot.strftime("%Y-%m-%d %H:%M"))

    return slots


# ============================================================================
# BUILD NORMALIZED DOCTOR DATABASE
# ============================================================================

def load_doctors():
    doctor_map = {}

    for disease, doctors in DOCTORS_RAW.items():
        for doc in doctors:
            doctor_id = slugify(doc["doctor"])

            if doctor_id not in doctor_map:
                doctor_map[doctor_id] = {
                    "id": doctor_id,
                    "name": doc["doctor"],
                    "gender": doc["gender"],
                    "hospital": doc["hospital"],
                    "location": doc["hospital_city"],
                    "specialty": doc["department"],
                    "experience": doc["experience"],
                    "price_min": doc["consultation_fee_min"],
                    "price_max": doc["consultation_fee_max"],
                    "working_days": doc["working_days"],
                    "time": doc["time"],
                    "expertise": set(),
                    "available_slots": generate_available_slots(
                        doc["working_days"],
                        doc["time"]
                    )
                }

            doctor_map[doctor_id]["expertise"].add(disease.lower())

    return list(doctor_map.values())


DOCTORS_DB = load_doctors()


# ============================================================================
# TOOL: SEARCH DOCTORS
# ============================================================================

@tool
def search_doctors(
    symptoms: str,
    location: str = "",
    specialty: str = "",
    max_price: int = 9999999,
    gender_preference: str = ""
) -> str:
    """
    Search doctors by symptoms and preferences.

    Example:
    search_doctors(
        symptoms="đau họng và ho",
        location="Hà Nội",
        max_price=400000,
        gender_preference="Nữ"
    )
    """

    symptoms_lower = symptoms.lower()

    matched_diseases = set()

    for symptom, disease_info in DISEASES_DB.items():
        if symptom_matches(symptoms_lower, symptom):
            matched_diseases.add(disease_info["disease"].lower())

    normalized_specialty = normalize_specialty(specialty) if specialty else ""
    normalized_gender = normalize_gender(gender_preference) if gender_preference else ""

    results = []

    for doctor in DOCTORS_DB:
        disease_match = (
            not matched_diseases
            or any(disease in doctor["expertise"] for disease in matched_diseases)
        )

        location_match = (
            not location
            or location.lower() in doctor["location"].lower()
        )

        specialty_match = (
            not normalized_specialty
            or normalized_specialty in doctor["specialty"].lower()
        )

        gender_match = (
            not normalized_gender
            or normalize_gender(doctor["gender"]) == normalized_gender
        )

        price_match = doctor["price_min"] <= max_price

        if (
            disease_match
            and location_match
            and specialty_match
            and gender_match
            and price_match
        ):
            results.append(doctor)

    if not results and specialty:
        for doctor in DOCTORS_DB:
            if (
                normalized_specialty in doctor["specialty"].lower()
                and (not location or location.lower() in doctor["location"].lower())
                and doctor["price_min"] <= max_price
            ):
                results.append(doctor)

    if not results:
        return (
            "❌ Không tìm thấy bác sĩ phù hợp.\n\n"
            f"- Triệu chứng: {symptoms}\n"
            f"- Địa điểm: {location or 'Bất kỳ'}\n"
            f"- Chuyên khoa: {specialty or 'Bất kỳ'}\n"
            f"- Ngân sách tối đa: {max_price:,}đ\n\n"
            "Gợi ý:\n"
            "- Thử bỏ lọc giới tính\n"
            "- Tăng ngân sách\n"
            "- Chọn địa điểm khác"
        )

    results.sort(
        key=lambda d: (
            d["location"] != "Hà Nội",
            d["price_min"],
            -d["experience"]
        )
    )

    output = [f"✅ Tìm thấy {len(results)} bác sĩ phù hợp:\n"]

    for idx, doctor in enumerate(results, 1):
        diseases = ", ".join(sorted(doctor["expertise"]))

        output.append(
            f"{idx}. {doctor['name']}\n"
            # f"   🆔 ID: {doctor['id']}\n"
            f"   🏥 Bệnh viện: {doctor['hospital']}\n"
            f"   📍 Thành phố: {doctor['location']}\n"
            f"   🩺 Chuyên khoa: {doctor['specialty']}\n"
            f"   👤 Giới tính: {doctor['gender']}\n"
            f"   📚 Kinh nghiệm: {doctor['experience']} năm\n"
            f"   💰 Giá khám: {doctor['price_min']:,}đ - {doctor['price_max']:,}đ\n"
            f"   🎯 Phù hợp với: {diseases}\n"
        )

    return "\n".join(output)


# ============================================================================
# TOOL: CHECK AVAILABILITY
# ============================================================================

@tool
def check_availability(doctor_id: str, preferred_day: str = "") -> str:
    """
    Check doctor's available schedule.

    Example:
    check_availability("nguyen_minh_anh")
    check_availability("nguyen_minh_anh", "thứ 6")
    """

    doctor = next((d for d in DOCTORS_DB if d["id"] == doctor_id), None)

    if not doctor:
        return f"❌ Không tìm thấy bác sĩ với ID: {doctor_id}"

    slots = doctor["available_slots"]

    if preferred_day:
        preferred_day = preferred_day.strip().lower()

        if preferred_day not in DAY_MAPPING:
            return (
                "❌ Ngày không hợp lệ. Ví dụ: thứ 2, thứ 3, ..., chủ nhật"
            )

        weekday_target = DAY_MAPPING[preferred_day]

        filtered_slots = []
        for slot in slots:
            slot_dt = datetime.strptime(slot, "%Y-%m-%d %H:%M")
            if slot_dt.isoweekday() == weekday_target:
                filtered_slots.append(slot)

        slots = filtered_slots

    if not slots:
        return (
            f"❌ Bác sĩ {doctor['name']} không còn lịch trống"
            f" {preferred_day if preferred_day else ''}."
        )

    preview_slots = slots[:10]

    result = [
        f"📅 Lịch khám của {doctor['name']} - {doctor['hospital']}:",
        ""
    ]

    for idx, slot in enumerate(preview_slots, 1):
        result.append(f"{idx}. {slot}")

    if len(slots) > 10:
        result.append(f"\n... và còn {len(slots) - 10} lịch khác")

    return "\n".join(result)


# ============================================================================
# TOOL: BOOK APPOINTMENT
# ============================================================================

@tool
def book_appointment(
    doctor_id: str,
    appointment_time: str,
    patient_name: str,
    phone: str
) -> str:
    """
    Book appointment.

    Example:
    book_appointment(
        doctor_id="nguyen_minh_anh",
        appointment_time="2026-04-10 09:00",
        patient_name="Nguyễn Văn A",
        phone="0901234567"
    )
    """

    doctor = next((d for d in DOCTORS_DB if d["id"] == doctor_id), None)

    if not doctor:
        return f"❌ Không tìm thấy bác sĩ với ID: {doctor_id}"

    if appointment_time not in doctor["available_slots"]:
        return (
            f"❌ Khung giờ {appointment_time} không còn trống.\n"
            "Hãy dùng check_availability để xem lịch mới nhất."
        )

    doctor["available_slots"].remove(appointment_time)

    confirmation_code = (
        f"VIN-"
        f"{doctor['id'].upper()}-"
        f"{appointment_time.replace('-', '').replace(':', '').replace(' ', '')}"
    )

    return (
        "✅ Đặt lịch thành công!\n\n"
        f"📋 Mã xác nhận: {confirmation_code}\n"
        f"👤 Bệnh nhân: {patient_name}\n"
        f"📞 Số điện thoại: {phone}\n"
        f"👨‍⚕️ Bác sĩ: {doctor['name']}\n"
        f"🏥 Bệnh viện: {doctor['hospital']}\n"
        f"🩺 Chuyên khoa: {doctor['specialty']}\n"
        f"📍 Địa điểm: {doctor['location']}\n"
        f"🕒 Thời gian: {appointment_time}\n"
        f"💰 Chi phí dự kiến: {doctor['price_min']:,}đ - {doctor['price_max']:,}đ\n\n"
        "💡 Vui lòng đến trước 10 phút và mang CCCD/CMND."
    )

