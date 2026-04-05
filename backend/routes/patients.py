from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from extensions import db
from models import Patient, Appointment, Doctor, MedicalRecord, Vital, Review, Prescription, Note
from datetime import datetime
import json

patient_bp = Blueprint("patients", __name__)




# -----------------------------
# Patient Profile
# -----------------------------
@patient_bp.route("/patients/me", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_my_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.get(user_id)

    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404
        
    try:
        preferences = json.loads(patient.preferences) if patient.preferences else []
    except:
        preferences = []

    profile = {
        "_id": str(patient.id),
        "fullName": patient.name,
        "email": patient.email,
        "phone": patient.mobile,
        "dob": patient.dob,
        "address": patient.address,
        "blood_type": patient.blood_type
    }
    
    return jsonify({"profile": profile, "preferences": preferences})


# ------------------------------
# Patient Update Profile
# ------------------------------
@patient_bp.route("/patients/update", methods=["PUT"])
@jwt_required()
@role_required("Patient")
def update_patient():
    user_id = int(get_jwt_identity())
    data = request.json
    
    patient = Patient.query.get(user_id)
    if not patient:
         return jsonify({"error": "Not found"}), 404
         
    if "fullName" in data: patient.name = data["fullName"]
    if "phone" in data: patient.mobile = data["phone"]
    if "dob" in data: patient.dob = data["dob"]
    if "address" in data: patient.address = data["address"]
    if "blood_type" in data: patient.blood_type = data["blood_type"]
    
    if not any(k in data for k in ["fullName", "phone", "dob", "address"]):
        if "name" in data: patient.name = data["name"]
        if "mobile" in data: patient.mobile = data["mobile"]
        if "age" in data: patient.age = data["age"]
        if "gender" in data: patient.gender = data["gender"]
    
    db.session.commit()
    return jsonify({"message": "Profile updated"})




# -----------------------------
# Patient Dashboard
# -----------------------------
@patient_bp.route("/patients/dashboard", methods=["GET"])
@jwt_required()
@role_required("Patient")
def patient_dashboard():
    user_id = int(get_jwt_identity())
    now = datetime.utcnow()
    
    next_apt = Appointment.query.filter(Appointment.patient_id == user_id, Appointment.status != "Cancelled" ,Appointment.date >= now).order_by(Appointment.date.asc()).first()
    
    next_appointment = None
    if next_apt:
        diff = next_apt.date - now
        days, hours, mins = 0, 0, 0
        if diff:
            days = diff.days
            secs = diff.seconds
            hours = secs // 3600
            mins = (secs % 3600) // 60
            
        next_appointment = {
            "id": str(next_apt.id),
            "days": str(days).zfill(2),
            "hours": str(hours).zfill(2),
            "mins": str(mins).zfill(2),
            "doctorName": next_apt.doctor.name if next_apt.doctor else "Unknown Dr.",
            "doctorImage": next_apt.doctor.image_url if next_apt.doctor and next_apt.doctor.image_url else f"https://ui-avatars.com/api/?name={next_apt.doctor.name if next_apt.doctor else 'Doc'}",
            "type": next_apt.type,
            "dateFormatted": next_apt.date.strftime("%A, %b %d • %I:%M %p") if next_apt.date else "",
            "status": next_apt.status
        }
        
    vitals_db = Vital.query.filter_by(patient_id=user_id).limit(3).all()
    vitals = []
    for v in vitals_db:
        color = "bg-blue-600" if "Heart" in (v.label or "") else "bg-orange-500"
        icon = "❤️" if "Heart" in (v.label or "") else "💧"
        vitals.append({
            "label": v.label,
            "value": f"{v.value} {v.unit}",
            "pct": 70,
            "color": color,
            "icon": icon
        })
        
    return jsonify({"nextAppointment": next_appointment, "vitals": vitals})




# -----------------------------
# Doctors List
# -----------------------------
@patient_bp.route("/patients/doctors", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_doctors_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search')
    
    query = Doctor.query.filter_by(status="Active")
    if search:
        query = query.filter(db.or_(
            Doctor.name.ilike(f"%{search}%"),
            Doctor.specialization.ilike(f"%{search}%")
        ))
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = []
    for d in pagination.items:
        result.append({
            "id": str(d.id),
            "doctor_id": d.doctor_id,
            "name": d.name,
            "specialty": d.specialization,
            "clinic": d.clinic,
            "rating": d.rating,
            "reviews": d.reviews,
            "fee": d.fee,
            "online": d.online,
            "bio": d.bio,
            "image": d.image_url if d.image_url else f"https://ui-avatars.com/api/?name={d.name}"
        })
        
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        },
        "data": result
    })




# -----------------------------
# Doctor Profile
# -----------------------------
@patient_bp.route("/patients/doctors/<doc_id>", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_doctor_profile(doc_id):
    if doc_id.startswith("DOC-"):
        d = Doctor.query.filter_by(doctor_id=doc_id).first()
    else:
        d = Doctor.query.get(int(doc_id))
    if not d:
        return jsonify({"error": "Doctor not found"}), 404
        
    specializations = [d.specialization]
    
    doctor = {
        "id": str(d.id),
        "doctor_id": d.doctor_id,
        "name": d.name,
        "image": d.image_url if d.image_url else f"https://ui-avatars.com/api/?name={d.name}",
        "title": d.specialization,
        "education": d.education,
        "experience": f"{d.experience}+ Years",
        "languages": d.languages.split(",") if d.languages else ["English"],
        "rating": d.rating,
        "patientCount": "Verified",
        "reviews": f'{d.reviews}+',
        "fee": d.fee,
        "specializations": specializations,
        "bio_p1": d.bio,
        "bio_p2": ""
    }
    
    db_reviews = Review.query.filter_by(doctor_id=d.id).limit(5).all()
    reviews = []
    for r in db_reviews:
        reviews.append({
            "id": str(r.id),
            "author": r.author,
            "rating": r.rating,
            "date": r.date,
            "comment": r.comment
        })
        
    return jsonify({"doctor": doctor, "reviews": reviews})

# -----------------------------
# My Appointments
# -----------------------------
@patient_bp.route("/patients/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_my_appointments():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search')
    
    query = Appointment.query.join(Doctor).filter(Appointment.patient_id == user_id, Appointment.status != "Cancelled")
    if search:
        query = query.filter(db.or_(
            Doctor.name.ilike(f"%{search}%"),
            Doctor.specialization.ilike(f"%{search}%"),
            Appointment.type.ilike(f"%{search}%"),
            Appointment.status.ilike(f"%{search}%")
        ))
        
    pagination = query.order_by(Appointment.date.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    now = datetime.utcnow()
    upcoming = []
    past = []
    
    for apt in pagination.items:
        dt = apt.date
        if not dt: continue
        doc_name = apt.doctor.name if apt.doctor else "Unknown Dr."
        spec = apt.doctor.specialization if apt.doctor else "General"
        
        is_past = dt < now
        if is_past:
             past.append({
                "id": str(apt.id),
                "date": dt.strftime("%b %d, %Y"),
                "doctor": doc_name,
                "department": spec,
                "type": apt.type,
                "img": apt.doctor.image_url if apt.doctor and apt.doctor.image_url else f"https://ui-avatars.com/api/?name={doc_name}"
             })
        else:
             status = apt.status if apt.status else "Confirmed"
             status_class = "bg-orange-100 text-orange-600" if status.lower() == "pending" else "bg-green-100 text-green-600"
             upcoming.append({
                "id": str(apt.id),
                "month": dt.strftime("%b").upper(),
                "day": dt.strftime("%d"),
                "doctor": doc_name,
                "specialty": spec,
                "type": apt.type,
                "time": dt.strftime("%I:%M %p"),
                "status": status.capitalize(),
                "statusClass": status_class
             })
             
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        },
        "upcomingAppointments": upcoming,
        "pastVisits": past
    })




# -----------------------------
# Past Appointment Details
# -----------------------------
@patient_bp.route("/patients/appointments/<apt_id>", methods=["GET"])
@jwt_required()
@role_required("Patient")
def appointment_details(apt_id):
    if str(apt_id).startswith("APT-"):
        apt = Appointment.query.filter_by(appointment_id=apt_id).first()
    else:
        apt = Appointment.query.get(int(apt_id))
    if not apt: return jsonify({"error": "Appointment not found"}), 404
    
    dt = apt.date
    doc_info = apt.doctor
    
    details = {
        "dateFormatted": dt.strftime("%B %d, %Y") if dt else "Unknown Date",
        "doctorName": doc_info.name if doc_info else "Unknown Dr.",
        "doctorDepartment": doc_info.specialization if doc_info else "General",
        "doctorImage": doc_info.image_url if doc_info and doc_info.image_url else f"https://ui-avatars.com/api/?name={doc_info.name if doc_info else 'D'}",
        "diagnosisTitle": apt.diagnosisTitle,
        "diagnosisStatus": apt.status,
        "diagnosisDesc": apt.diagnosisDesc
    }
    
    prescriptions_db = Prescription.query.filter_by(appointment_id=apt.id).all()
    prescriptions = [{"name": p.name, "dosage": p.dosage, "frequency": p.frequency, "duration": p.duration} for p in prescriptions_db]
    
    notes_db = Note.query.filter_by(appointment_id=apt.id).all()
    notes = [{"text": n.text, "date": n.date} for n in notes_db]
    
    vitals_db = Vital.query.filter_by(appointment_id=apt.id).all()
    visitVitals = [{"label": v.label, "value": v.value, "unit": v.unit} for v in vitals_db]
    
    return jsonify({
        "details": details,
        "prescriptions": prescriptions,
        "notes": notes,
        "visitVitals": visitVitals
    })
    



# -----------------------------
# Medical History
# -----------------------------
@patient_bp.route("/patients/medical-history", methods=["GET"])
@jwt_required()
@role_required("Patient")
def medical_history():
    user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    per_page = 3 
    search = request.args.get('search')
    
    query = MedicalRecord.query.filter_by(patient_id=user_id).order_by(MedicalRecord.date.desc())
    
    if search:
        query = query.filter(db.or_(
            MedicalRecord.title.ilike(f"%{search}%"),
            MedicalRecord.description.ilike(f"%{search}%")
        ))
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    medicalRecords = []
    for r in pagination.items:
        medicalRecords.append({
            "id": str(r.id),
            "date": r.date, 
            "title": r.title,
            "description": r.description,
            "status": "Ready" 
        })
    
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "has_next": pagination.has_next 
        },
        "medicalRecords": medicalRecords
    })



# -----------------------------
# Add Doctor Review
# -----------------------------
@patient_bp.route("/patients/doctors/<doc_id>/review", methods=["POST"])
@jwt_required()
@role_required("Patient")
def add_review(doc_id):
    if doc_id.startswith("DOC-"):
        doc = Doctor.query.filter_by(doctor_id=doc_id).first()
    else:
        doc = Doctor.query.get(int(doc_id))
    if not doc: 
        return jsonify({"error": "Doctor not found"}), 404
    
    data = request.json
    user_id = int(get_jwt_identity())
    patient = Patient.query.get(user_id)
    
    new_rating = float(data.get("rating", 5.0))
    current_total_score = doc.rating * doc.reviews
    doc.reviews += 1
    doc.rating = round((current_total_score + new_rating) / doc.reviews, 1)

    r = Review(
        doctor_id=doc.id,
        author=patient.name if patient else "Anonymous",
        rating=new_rating,
        comment=data.get("comment", "")
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"message": "Review added successfully"}), 201




# -----------------------------
# Export Medical History in CSV
# -----------------------------
@patient_bp.route("/patients/export-csv", methods=["POST"])
@jwt_required()
@role_required("Patient")
def trigger_export_csv():
    pass