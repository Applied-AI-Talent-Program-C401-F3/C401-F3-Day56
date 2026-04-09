from langchain_core.tools import tool
import json
import re

# ===========================================================================
# LOAD DOCTOR DATABASE FROM database.md
# ===========================================================================

def load_doctors_from_markdown():
    """Load doctor data from database.md"""
    with open("database.json", "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON from markdown code block
    match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    return []

DOCTORS_DB = load_doctors_from_markdown()

# ===========================================================================
# TOOLS
# ===========================================================================

@tool
def search_doctors(symptoms: str, location: str = "", specialty: str = "", max_price: int = 9999999, gender_preference: str = "") -> str:
    """
    Search for suitable doctors based on patient symptoms, location, and preferences.

    Parameters:
    - symptoms: Patient's symptoms or health concerns (e.g., 'chest pain', 'fever and cough')
    - location: Preferred city/location (optional) (e.g., 'Hà Nội', 'TP.HCM', 'Đà Nẵng')
    - specialty: Preferred medical specialty (optional) (e.g., 'Nội khoa', 'Tim mạch')
    - max_price: Maximum budget for consultation in VND (optional, default: no limit)
    - gender_preference: Preferred doctor gender - 'Male' or 'Female' (optional)

    Returns:
    A list of recommended doctors with details: name, specialty, experience, price range, location, and availability.
    """

    symptoms_lower = symptoms.lower()
    matches = []

    # Filter doctors based on criteria
    for doctor in DOCTORS_DB:
        # Check symptom match via expertise keywords
        symptom_match = any(keyword in symptoms_lower for keyword in doctor['expertise_keywords'])

        # Check location match
        location_match = (not location) or (location.lower() in doctor['location'].lower())

        # Check specialty match
        specialty_match = (not specialty) or (specialty.lower() in doctor['specialty'].lower())

        # Check price match
        price_match = (doctor['price_max'] <= max_price)

        # Check gender preference
        gender_match = (not gender_preference) or (gender_preference.lower() == doctor['attributes']['gender'].lower())

        # If matches all criteria
        if symptom_match and location_match and specialty_match and price_match and gender_match:
            matches.append(doctor)

    # If no exact symptom matches, suggest doctors from relevant specialty
    if not matches and specialty:
        for doctor in DOCTORS_DB:
            location_match = (not location) or (location.lower() in doctor['location'].lower())
            specialty_match = (specialty.lower() in doctor['specialty'].lower())
            price_match = doctor['price_max'] <= max_price
            if location_match and specialty_match and price_match:
                matches.append(doctor)

    if not matches:
        return f"❌ Không tìm thấy bác sỹ phù hợp với yêu cầu của bạn (Triệu chứng: {symptoms}, Địa điểm: {location or 'Bất kỳ'}, Chuyên khoa: {specialty or 'Bất kỳ'}).\n\nHãy thử điều chỉnh:\n- Thay đổi địa điểm\n- Tăng ngân sách\n- Chọn chuyên khoa khác"

    # Format results
    result = f"✅ Tìm thấy {len(matches)} bác sỹ phù hợp:\n\n"

    for i, doc in enumerate(matches, 1):
        price_min_formatted = f"{doc['price_min']:,.0f}".replace(",", ".")
        price_max_formatted = f"{doc['price_max']:,.0f}".replace(",", ".")
        exp = doc['attributes']['years_experience']
        gender = doc['attributes']['gender']

        result += f"{i}. {doc['name']}\n"
        result += f"   🏥 Chuyên khoa: {doc['specialty']}\n"
        result += f"   👤 Giới tính: {gender}\n"
        result += f"   📚 Kinh nghiệm: {exp} năm\n"
        result += f"   💰 Giá khám: {price_min_formatted}đ - {price_max_formatted}đ\n"
        result += f"   📍 Địa điểm: {doc['location']}\n"
        result += f"   🆔 ID: {doc['id']}\n\n"

    return result


@tool
def check_availability(doctor_id: str, preferred_date: str = "") -> str:
    """
    Check available appointment slots for a specific doctor.

    Parameters:
    - doctor_id: The doctor's ID (e.g., 'D001', 'D002')
    - preferred_date: Preferred date in format YYYY-MM-DD (optional, for filtering)

    Returns:
    List of available time slots for the doctor.
    """

    # Find doctor
    doctor = next((d for d in DOCTORS_DB if d['id'] == doctor_id), None)

    if not doctor:
        return f"❌ Không tìm thấy bác sỹ với ID: {doctor_id}"

    slots = doctor['available_slots']

    # Filter by date if provided
    if preferred_date:
        slots = [slot for slot in slots if slot.startswith(preferred_date)]

    if not slots:
        return f"❌ Không có lịch khám trống cho bác sỹ {doctor['name']} vào ngày {preferred_date or 'được yêu cầu'}."

    result = f"📅 Lịch khám trống của {doctor['name']} ({doctor['specialty']}):\n\n"
    for i, slot in enumerate(slots, 1):
        result += f"{i}. {slot}\n"

    return result


@tool
def book_appointment(doctor_id: str, appointment_time: str, patient_name: str, phone: str) -> str:
    """
    Book an appointment with a doctor.

    Parameters:
    - doctor_id: The doctor's ID (e.g., 'D001')
    - appointment_time: Appointment time in format YYYY-MM-DD HH:MM (e.g., '2026-04-09 09:00')
    - patient_name: Patient's full name
    - phone: Patient's phone number

    Returns:
    Appointment confirmation with details.
    """

    # Find doctor
    doctor = next((d for d in DOCTORS_DB if d['id'] == doctor_id), None)

    if not doctor:
        return f"❌ Không tìm thấy bác sỹ với ID: {doctor_id}"

    # Check if slot exists
    if appointment_time not in doctor['available_slots']:
        return f"❌ Lịch khám {appointment_time} không còn trống. Vui lòng chọn lịch khác."

    # Generate confirmation
    confirmation_code = f"VIN{doctor_id}{appointment_time.replace('-', '').replace(':', '').replace(' ', '')}"

    price_min_formatted = f"{doctor['price_min']:,.0f}".replace(",", ".")
    price_max_formatted = f"{doctor['price_max']:,.0f}".replace(",", ".")

    result = f"✅ Đặt lịch khám thành công!\n\n"
    result += f"📋 Chi tiết xác nhận:\n"
    result += f"- Mã xác nhận: {confirmation_code}\n"
    result += f"- Bác sỹ: {doctor['name']}\n"
    result += f"- Chuyên khoa: {doctor['specialty']}\n"
    result += f"- Thời gian: {appointment_time}\n"
    result += f"- Địa điểm: {doctor['location']}\n"
    result += f"- Bệnh nhân: {patient_name}\n"
    result += f"- Điện thoại: {phone}\n"
    result += f"- Giá khám: {price_min_formatted}đ - {price_max_formatted}đ\n\n"
    result += f"💡 Vui lòng đến 10 phút trước giờ khám. Mang theo CMND/căn cước công dân."

    return result
