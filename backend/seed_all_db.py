import os
import random
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

print("Connected! Updating existing collections...")

# 1. Update Existing Doctors
doctors = list(db.doctors.find())
for doc in doctors:
    update_fields = {}
    if "clinic" not in doc: update_fields["clinic"] = "Central Medical Hospital"
    if "rating" not in doc: update_fields["rating"] = round(random.uniform(4.0, 5.0), 1)
    if "reviews" not in doc: update_fields["reviews"] = random.randint(50, 300)
    if "fee" not in doc: update_fields["fee"] = doc.get("experience", 10) * 15
    if "online" not in doc: update_fields["online"] = random.choice([True, False])
    if "education" not in doc: update_fields["education"] = "MD - Top Medical Univ"
    if "languages" not in doc: update_fields["languages"] = ["English", "Spanish"]
    if "bio" not in doc: update_fields["bio"] = f"Dr. {doc.get('name')} is an expert {doc.get('specialization', 'specialist')} dedicated to patient care."
    if "specializations" not in doc: 
        update_fields["specializations"] = [doc.get("specialization", "General"), "Preventive Care", "Consulting"]
    
    if update_fields:
        db.doctors.update_one({"_id": doc["_id"]}, {"$set": update_fields})
print("✅ Doctors updated")

# 2. Update Existing Patients
patients = list(db.patients.find())
for pat in patients:
    update_fields = {}
    if "dob" not in pat: update_fields["dob"] = "1990-05-15"
    if "address" not in pat: update_fields["address"] = "123 Health Ave, NY"
    if "preferences" not in pat: 
        update_fields["preferences"] = [
            {"label": "Appointment Reminders", "enabled": True},
            {"label": "Lab Results", "enabled": True}
        ]
    
    if update_fields:
        db.patients.update_one({"_id": pat["_id"]}, {"$set": update_fields})
print("✅ Patients updated")

# 3. Update Existing Appointments
appointments = list(db.appointments.find())
for apt in appointments:
    update_fields = {}
    if "type" not in apt: update_fields["type"] = "General Checkup"
    if "location" not in apt: update_fields["location"] = "Main Hospital, Wing " + random.choice(["A", "B", "C"])
    
    if update_fields:
        db.appointments.update_one({"_id": apt["_id"]}, {"$set": update_fields})
print("✅ Appointments updated")


print("Seeding relationship collections for all appointments...")

# Wipe the mock collections created in the last step to regenerate complete ones
db.vitals.delete_many({})
db.prescriptions.delete_many({})
db.notes.delete_many({})
db.medical_records.delete_many({})
db.reviews.delete_many({})

prescriptions, notes, vitals, medical_records, reviews = [], [], [], [], []

for apt in appointments:
    apt_id = apt["_id"]
    pat_id = apt.get("patient_id")
    doc_id = apt.get("doctor_id")
    
    if not pat_id or not doc_id: continue
    
    # Prescriptions
    prescriptions.append({
        "appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id,
        "name": 'Cetirizine', "strength": '10 mg', "type": 'Oral Tablet', "dosage": '1 tablet daily', "refills": 1
    })
    
    # Notes
    notes.append({
        "appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id, 
        "title": 'Next Steps', "content": 'Maintain healthy diet and regular cardiovascular activity.'
    })
    
    # Vitals
    vitals.extend([
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Blood Pressure', "value": '120/80', "unit": 'mmHg'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Heart Rate', "value": str(random.randint(65, 85)), "unit": 'bpm'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Temperature', "value": '98.6', "unit": '°F'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Oxygen Sat.', "value": '99', "unit": '%'}
    ])
    
    # Medical records
    medical_records.append({
        "appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id, "type": 'Clinical Visit', 
        "date": apt.get("date").strftime("%b %d, %Y") if apt.get("date") else "Unknown Date", 
        "time": "10:00 AM",
        "title": 'General Assessment', "description": 'Routine checkup completed smoothly. Patient vital signs normal.',
        "provider": 'Central Clinic', "status": 'Ready', "icon": '🏥',
        "markerClass": 'text-blue-600 ring-4 ring-blue-50', "tagClass": 'bg-blue-50 text-blue-600', "actionLabel": 'Notes PDF'
    })

# Add some global reviews for doctors
for doc in doctors:
    for pat in patients[:2]:  # Link 2 reviews per doctor max using existing patients
        reviews.append({
            "doctor_id": doc["_id"], "patient_id": pat["_id"], "author": pat.get("name", "Patient"), 
            "rating": 5, "date": "1 week ago", "comment": "Excellent doctor, highly recommend. Very thorough!"
        })

if prescriptions: db.prescriptions.insert_many(prescriptions)
if notes: db.notes.insert_many(notes)
if vitals: db.vitals.insert_many(vitals)
if medical_records: db.medical_records.insert_many(medical_records)
if reviews: db.reviews.insert_many(reviews)

print("✅ Huge success! Database is completely fully seeded and structurally complete.")
