from langchain_core.tools import tool
import json

# ===========================================================================
# LOAD DOCTOR DATABASE FROM database.json
# ===========================================================================

def load_data_from_json():
    """Load all data from database.json"""
    with open("database.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_available_slots(working_days, time_range):
    """Generate available appointment slots based on working days and time range"""
    from datetime import datetime, timedelta

    if not working_days or not time_range:
        return []

    slots = []
    start_date = datetime.now()

    # Generate slots for the next 30 days
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        weekday = current_date.weekday() + 1  # Python weekday: 0=Monday, convert to 1=Monday

        # Check if this day is a working day
        if weekday in working_days:
            # Parse time range (e.g., "08:00-16:00")
            try:
                start_time, end_time = time_range.split('-')
                start_hour = int(start_time.split(':')[0])
                end_hour = int(end_time.split(':')[0])

                # Generate 1-hour slots
                for hour in range(start_hour, end_hour):
                    slot_time = f"{hour:02d}:00"
                    date_str = current_date.strftime("%Y-%m-%d")
                    slots.append(f"{date_str} {slot_time}")
            except:
                pass

    return slots

def load_doctors_from_json():
    """Load doctor data from database.json"""
    data = load_data_from_json()
    doctors_db = data["DOCTORS_DB"]
    day_mapping = data.get("DAY_MAPPING", {})

    # Flatten the doctors structure from {disease: [doctors]} to [doctors]
    # and map field names to expected format
    all_doctors = []
    doctor_counter = 1

    for disease, doctors_list in doctors_db.items():
        for doc in doctors_list:
            # Generate unique ID
            doctor_id = f"D{doctor_counter:03d}"
            doctor_counter += 1

            # Generate available slots based on working_days and time
            available_slots = generate_available_slots(
                doc.get("working_days", []),
                doc.get("time", "")
            )

            # Map database fields to expected field names
            mapped_doc = {
                "name": doc["doctor"],
                "specialty": doc["department"],
                "location": doc["hospital_city"],
                "price_min": doc["consultation_fee_min"],
                "price_max": doc["consultation_fee_max"],
                "id": doctor_id,
                "attributes": {
                    "gender": doc["gender"],
                    "years_experience": doc["experience"]
                },
                "expertise_keywords": [disease.lower()],  # Use disease name as keyword
                "available_slots": available_slots,
                "working_days": doc.get("working_days", []),
                "time": doc.get("time", ""),
                "hospital": doc.get("hospital", "")
            }
            all_doctors.append(mapped_doc)
    return all_doctors

DOCTORS_DB = load_doctors_from_json()
DATA = load_data_from_json()  # For accessing disease mappings

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

    # Map symptoms to diseases using the disease database
    diseases_db = DATA.get("DISEASES_DB", {})
    matched_diseases = set()
    for symptom_keyword, disease_info in diseases_db.items():
        if symptom_keyword in symptoms_lower:
            matched_diseases.add(disease_info["disease"].lower())

    # Filter doctors based on criteria
    for doctor in DOCTORS_DB:
        # Check symptom match via expertise keywords or disease mapping
        symptom_match = (
            any(keyword in symptoms_lower for keyword in doctor['expertise_keywords']) or
            any(keyword in matched_diseases for keyword in doctor['expertise_keywords'])
        )

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
