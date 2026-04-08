# Vinmec Medical Doctor Database

## Overview
Database of 20 Vietnamese doctors across 12 specialties for the Vinmec Medical Assistant.

## Doctor Data (JSON Format)

```json
[
  {
    "id": "D001",
    "name": "Dr. Nguyễn Anh Tuấn",
    "specialty": "Nội khoa",
    "expertise_keywords": ["fever", "cough", "fatigue", "chest pain", "blood pressure", "diabetes", "infection"],
    "price_min": 500000,
    "price_max": 800000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 15, "department": "Internal Medicine"},
    "available_slots": ["2026-04-09 09:00", "2026-04-09 10:30", "2026-04-10 14:00", "2026-04-11 15:30"]
  },
  {
    "id": "D002",
    "name": "Dr. Trần Minh Hương",
    "specialty": "Nội khoa",
    "expertise_keywords": ["headache", "dizziness", "fatigue", "infection", "chronic disease", "fever"],
    "price_min": 600000,
    "price_max": 900000,
    "location": "TP.HCM",
    "attributes": {"gender": "Female", "years_experience": 12, "department": "Internal Medicine"},
    "available_slots": ["2026-04-09 10:00", "2026-04-09 13:00", "2026-04-10 09:30", "2026-04-12 16:00"]
  },
  {
    "id": "D003",
    "name": "Dr. Phạm Quốc Minh",
    "specialty": "Nhi khoa",
    "expertise_keywords": ["child fever", "cough in children", "diarrhea", "malnutrition", "vaccine", "growth delay"],
    "price_min": 400000,
    "price_max": 700000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 10, "department": "Pediatrics"},
    "available_slots": ["2026-04-09 08:00", "2026-04-09 11:00", "2026-04-10 10:00", "2026-04-11 14:30"]
  },
  {
    "id": "D004",
    "name": "Dr. Võ Thị Kim Anh",
    "specialty": "Nhi khoa",
    "expertise_keywords": ["child development", "autism screening", "childhood asthma", "eczema", "allergy in children"],
    "price_min": 450000,
    "price_max": 750000,
    "location": "Đà Nẵng",
    "attributes": {"gender": "Female", "years_experience": 8, "department": "Pediatrics"},
    "available_slots": ["2026-04-09 09:30", "2026-04-10 11:00", "2026-04-11 09:00", "2026-04-12 13:00"]
  },
  {
    "id": "D005",
    "name": "Dr. Hoàng Thị Lan",
    "specialty": "Sản phụ khoa",
    "expertise_keywords": ["pregnancy", "prenatal care", "menstrual issues", "hormonal imbalance", "gynecological exam"],
    "price_min": 700000,
    "price_max": 1200000,
    "location": "TP.HCM",
    "attributes": {"gender": "Female", "years_experience": 18, "department": "Obstetrics & Gynecology"},
    "available_slots": ["2026-04-09 10:00", "2026-04-10 14:30", "2026-04-11 11:00", "2026-04-12 09:00"]
  },
  {
    "id": "D006",
    "name": "Dr. Lê Văn Hùng",
    "specialty": "Sản phụ khoa",
    "expertise_keywords": ["pregnancy complications", "delivery assistance", "women health", "fibroids", "infertility"],
    "price_min": 650000,
    "price_max": 1100000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 14, "department": "Obstetrics & Gynecology"},
    "available_slots": ["2026-04-09 14:00", "2026-04-10 09:00", "2026-04-11 15:00", "2026-04-12 10:30"]
  },
  {
    "id": "D007",
    "name": "Dr. Bùi Văn Khoa",
    "specialty": "Tâm thần",
    "expertise_keywords": ["depression", "anxiety", "stress", "insomnia", "bipolar disorder", "PTSD"],
    "price_min": 800000,
    "price_max": 1200000,
    "location": "TP.HCM",
    "attributes": {"gender": "Male", "years_experience": 16, "department": "Psychiatry"},
    "available_slots": ["2026-04-09 11:00", "2026-04-10 15:00", "2026-04-11 13:30", "2026-04-12 11:00"]
  },
  {
    "id": "D008",
    "name": "Dr. Ngô Thị Hà",
    "specialty": "Tâm thần",
    "expertise_keywords": ["anxiety disorder", "depression screening", "counseling", "behavioral issues", "trauma"],
    "price_min": 750000,
    "price_max": 1100000,
    "location": "Hà Nội",
    "attributes": {"gender": "Female", "years_experience": 11, "department": "Psychiatry"},
    "available_slots": ["2026-04-09 13:30", "2026-04-10 10:30", "2026-04-11 14:00", "2026-04-12 15:30"]
  },
  {
    "id": "D009",
    "name": "Dr. Đặng Anh Tuấn",
    "specialty": "Da liễu",
    "expertise_keywords": ["acne", "eczema", "psoriasis", "skin rash", "fungal infection", "aging skin"],
    "price_min": 600000,
    "price_max": 900000,
    "location": "TP.HCM",
    "attributes": {"gender": "Male", "years_experience": 13, "department": "Dermatology"},
    "available_slots": ["2026-04-09 09:00", "2026-04-10 13:00", "2026-04-11 10:00", "2026-04-12 14:30"]
  },
  {
    "id": "D010",
    "name": "Dr. Trương Ngọc Liên",
    "specialty": "Da liễu",
    "expertise_keywords": ["mole removal", "wart treatment", "sensitive skin", "vitiligo", "laser treatment"],
    "price_min": 700000,
    "price_max": 1000000,
    "location": "Đà Nẵng",
    "attributes": {"gender": "Female", "years_experience": 9, "department": "Dermatology"},
    "available_slots": ["2026-04-09 10:30", "2026-04-10 11:30", "2026-04-11 15:00", "2026-04-12 09:30"]
  },
  {
    "id": "D011",
    "name": "Dr. Lý Trung Hiếu",
    "specialty": "Tim mạch",
    "expertise_keywords": ["chest pain", "heart disease", "hypertension", "arrhythmia", "heart murmur", "ECG"],
    "price_min": 900000,
    "price_max": 1300000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 20, "department": "Cardiology"},
    "available_slots": ["2026-04-09 11:30", "2026-04-10 09:30", "2026-04-11 16:00", "2026-04-12 10:00"]
  },
  {
    "id": "D012",
    "name": "Dr. Vũ Thị Sao Mai",
    "specialty": "Tim mạch",
    "expertise_keywords": ["palpitations", "valvular disease", "heart failure", "stroke prevention", "angiography"],
    "price_min": 850000,
    "price_max": 1250000,
    "location": "TP.HCM",
    "attributes": {"gender": "Female", "years_experience": 17, "department": "Cardiology"},
    "available_slots": ["2026-04-09 14:00", "2026-04-10 14:30", "2026-04-11 11:30", "2026-04-12 13:00"]
  },
  {
    "id": "D013",
    "name": "Dr. Đinh Văn Linh",
    "specialty": "Nội tiết",
    "expertise_keywords": ["diabetes management", "thyroid disease", "metabolic disorder", "hormone imbalance", "obesity"],
    "price_min": 700000,
    "price_max": 1000000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 14, "department": "Endocrinology"},
    "available_slots": ["2026-04-09 10:00", "2026-04-10 15:30", "2026-04-11 09:30", "2026-04-12 14:00"]
  },
  {
    "id": "D014",
    "name": "Dr. Hà Minh Đức",
    "specialty": "Hô hấp",
    "expertise_keywords": ["asthma", "chronic bronchitis", "tuberculosis", "pneumonia", "shortness of breath", "lung cancer screening"],
    "price_min": 650000,
    "price_max": 950000,
    "location": "TP.HCM",
    "attributes": {"gender": "Male", "years_experience": 12, "department": "Respiratory"},
    "available_slots": ["2026-04-09 12:00", "2026-04-10 10:00", "2026-04-11 14:30", "2026-04-12 11:30"]
  },
  {
    "id": "D015",
    "name": "Dr. Tạ Quốc Bảo",
    "specialty": "Tiêu hóa",
    "expertise_keywords": ["stomach pain", "diarrhea", "constipation", "acid reflux", "gastritis", "ulcer"],
    "price_min": 600000,
    "price_max": 900000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 11, "department": "Gastroenterology"},
    "available_slots": ["2026-04-09 08:30", "2026-04-10 13:30", "2026-04-11 10:30", "2026-04-12 15:00"]
  },
  {
    "id": "D016",
    "name": "Dr. Chu Thị Thanh Tâm",
    "specialty": "Tiêu hóa",
    "expertise_keywords": ["liver disease", "hepatitis", "food poisoning", "irritable bowel syndrome", "colonoscopy"],
    "price_min": 700000,
    "price_max": 1000000,
    "location": "Đà Nẵng",
    "attributes": {"gender": "Female", "years_experience": 13, "department": "Gastroenterology"},
    "available_slots": ["2026-04-09 11:00", "2026-04-10 09:00", "2026-04-11 13:00", "2026-04-12 10:00"]
  },
  {
    "id": "D017",
    "name": "Dr. Tô Văn Sơn",
    "specialty": "Thận – Tiết niệu",
    "expertise_keywords": ["kidney disease", "urinary infection", "prostate issues", "kidney stones", "dialysis"],
    "price_min": 700000,
    "price_max": 1000000,
    "location": "TP.HCM",
    "attributes": {"gender": "Male", "years_experience": 16, "department": "Nephrology & Urology"},
    "available_slots": ["2026-04-09 14:30", "2026-04-10 11:00", "2026-04-11 15:30", "2026-04-12 09:00"]
  },
  {
    "id": "D018",
    "name": "Dr. Phan Thị Hương",
    "specialty": "Dị ứng – Miễn dịch lâm sàng",
    "expertise_keywords": ["allergic reaction", "food allergy", "hay fever", "asthma allergy", "autoimmune disease", "immunotherapy"],
    "price_min": 650000,
    "price_max": 950000,
    "location": "Hà Nội",
    "attributes": {"gender": "Female", "years_experience": 10, "department": "Allergy & Immunology"},
    "available_slots": ["2026-04-09 09:30", "2026-04-10 14:00", "2026-04-11 11:00", "2026-04-12 13:30"]
  },
  {
    "id": "D019",
    "name": "Dr. Ngô Văn Nam",
    "specialty": "Y học gia đình",
    "expertise_keywords": ["general health", "family care", "preventive medicine", "chronic disease management", "health screening"],
    "price_min": 400000,
    "price_max": 600000,
    "location": "Hà Nội",
    "attributes": {"gender": "Male", "years_experience": 18, "department": "Family Medicine"},
    "available_slots": ["2026-04-09 07:30", "2026-04-10 08:00", "2026-04-11 09:00", "2026-04-12 08:30"]
  },
  {
    "id": "D020",
    "name": "Dr. Huỳnh Thị Bích Ngọc",
    "specialty": "Y học gia đình",
    "expertise_keywords": ["routine checkup", "vaccination", "minor injury", "wellness counseling", "nutrition advice"],
    "price_min": 450000,
    "price_max": 650000,
    "location": "TP.HCM",
    "attributes": {"gender": "Female", "years_experience": 9, "department": "Family Medicine"},
    "available_slots": ["2026-04-09 08:00", "2026-04-10 10:30", "2026-04-11 10:00", "2026-04-12 14:30"]
  }
]
```

## Specialties

| Vietnamese | English |
|-----------|---------|
| Nội khoa | Internal Medicine |
| Nhi khoa | Pediatrics |
| Sản phụ khoa | Obstetrics & Gynecology |
| Tâm thần | Psychiatry |
| Da liễu | Dermatology |
| Tim mạch | Cardiology |
| Nội tiết | Endocrinology |
| Hô hấp | Respiratory |
| Tiêu hóa | Gastroenterology |
| Thận – Tiết niệu | Nephrology & Urology |
| Dị ứng – Miễn dịch lâm sàn | Allergy & Immunology |
| Y học gia đình | Family Medicine |

## Data Structure

Each doctor record contains:
- **id**: Unique identifier (D001-D020)
- **name**: Doctor's full name
- **specialty**: Medical specialty
- **expertise_keywords**: List of symptom/condition keywords for matching
- **price_min**: Minimum consultation price (VND)
- **price_max**: Maximum consultation price (VND)
- **location**: City/location (Hà Nội, TP.HCM, Đà Nẵng)
- **attributes**: Gender, years of experience, department name
- **available_slots**: List of available appointment times (YYYY-MM-DD HH:MM format)
