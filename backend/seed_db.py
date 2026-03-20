import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load local environment variables (.env)
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("Error: MONGO_URI not found.")
    exit(1)

# Connect to the MongoDB cluster securely using the Mongo URI
client = MongoClient(MONGO_URI)
db = client.get_default_database()

print("Connected to MongoDB safely! Checking collections...")

# Find the first doctor, patient, and appointment to link our mock data
doctor = db.doctors.find_one()
patient = db.patients.find_one()
appointment = db.appointments.find_one()

if not doctor or not patient or not appointment:
    print("WARNING: Could not find at least one Doctor, Patient, and Appointment in the database yet to link records to. Aborting mock insertion.")
    exit(0)

doc_id = doctor['_id']
pat_id = patient['_id']
apt_id = appointment['_id']

# 1. Insert Prescriptions Safely (Only if empty)
if "prescriptions" not in db.list_collection_names() or db.prescriptions.count_documents({}) == 0:
    db.prescriptions.insert_many([
        {
            "appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id,
            "name": 'Cetirizine', "strength": '10 mg', "type": 'Oral Tablet', "dosage": '1 tablet daily', "refills": 1
        },
        {
            "appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id,
            "name": 'Fluticasone Propionate (Flonase)', "strength": '50 mcg/actuation', "type": 'Nasal Spray', "dosage": '2 sprays in each nostril once daily', "refills": 3
        }
    ])
    print("✅ Seeded new 'prescriptions' collection")
else:
    print("⏭️ 'prescriptions' collection already contains data, skipping insertion.")

# 2. Insert Notes Safely
if "notes" not in db.list_collection_names() or db.notes.count_documents({}) == 0:
    db.notes.insert_many([
        {"appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id, "title": 'Next Steps', "content": 'Maintain healthy diet and regular exercise. Increase fluid intake.'},
        {"appointment_id": apt_id, "patient_id": pat_id, "doctor_id": doc_id, "title": 'Follow-Up', "content": 'Schedule a review in 6 months.'}
    ])
    print("✅ Seeded new 'notes' collection")
else:
    print("⏭️ 'notes' collection already contains data, skipping insertion.")

# 3. Insert Vitals Safely
if "vitals" not in db.list_collection_names() or db.vitals.count_documents({}) == 0:
    db.vitals.insert_many([
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Blood Pressure', "value": '120/80', "unit": 'mmHg'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Heart Rate', "value": '72', "unit": 'bpm'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Temperature', "value": '98.6', "unit": '°F'},
        {"appointment_id": apt_id, "patient_id": pat_id, "label": 'Oxygen Sat.', "value": '99', "unit": '%'}
    ])
    print("✅ Seeded new 'vitals' collection")
else:
    print("⏭️ 'vitals' collection already contains data, skipping insertion.")

# 4. Insert Medical Records Safely
if "medical_records" not in db.list_collection_names() or db.medical_records.count_documents({}) == 0:
    db.medical_records.insert_many([
        {
            "patient_id": pat_id, "doctor_id": doc_id, "type": 'Lab Report', "date": 'Oct 24, 2023', "time": '09:15 AM',
            "title": 'Comprehensive Blood Panel', "description": 'Routine checkup. Results indicate normal ranges.',
            "provider": 'City General Lab', "status": 'Ready', "icon": '🔬',
            "markerClass": 'text-green-600 ring-4 ring-green-50', "tagClass": 'bg-green-50 text-green-600', "actionLabel": 'Download PDF'
        },
        {
            "patient_id": pat_id, "doctor_id": doc_id, "type": 'Clinical Visit', "date": 'Oct 12, 2023', "time": '02:30 PM',
            "title": 'Cardiology Consultation', "description": 'Follow-up appointment. Heart sounds normal.',
            "provider": 'Heart & Wellness Clinic', "status": 'Ready', "icon": '🏥',
            "markerClass": 'text-blue-600 ring-4 ring-blue-50', "tagClass": 'bg-blue-50 text-blue-600', "actionLabel": 'Notes PDF'
        }
    ])
    print("✅ Seeded new 'medical_records' collection")
else:
    print("⏭️ 'medical_records' collection already contains data, skipping insertion.")

# 5. Insert Reviews Safely
if "reviews" not in db.list_collection_names() or db.reviews.count_documents({}) == 0:
    db.reviews.insert_many([
        {"doctor_id": doc_id, "patient_id": pat_id, "author": "Michael R.", "rating": 5, "date": "2 days ago", "comment": "Incredibly thorough and explained everything."},
        {"doctor_id": doc_id, "patient_id": pat_id, "author": "Elena K.", "rating": 5, "date": "1 week ago", "comment": "Exceptional care and attention."}
    ])
    print("✅ Seeded new 'reviews' collection")
else:
    print("⏭️ 'reviews' collection already contains data, skipping insertion.")

print("\n🚀 Seeding finished smoothly. No existing user, appointment, or doctor records were deleted or touched whatsoever.")
