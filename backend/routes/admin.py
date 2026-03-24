from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from utils import role_required, get_next_doctor_id
from datetime import datetime, timedelta
import math
from extensions import db
from models import Doctor, Patient, Appointment

admin_bp = Blueprint("admin", __name__)




# -----------------------------
# Get Stats
# -----------------------------
@admin_bp.route("/admin",methods=["GET"])
@jwt_required()
@role_required("Admin")
def stats():
    total = Doctor.query.count()
    active = Doctor.query.filter_by(status="Active").count()
    inactive = Doctor.query.filter_by(status="Inactive").count()
    on_leave = Doctor.query.filter_by(status="On Leave").count()
    patients = Patient.query.count()
    appointments = Appointment.query.count()

    return jsonify({
        "total_doctors": total,
        "total_active_doctors": active,
        "total_inactive_doctors": inactive,
        "total_onleave_doctors": on_leave,
        "total_patients": patients,
        "total_appointments": appointments
    }), 200





# -----------------------------
# Add Doctor
# -----------------------------
@admin_bp.route("/admin/add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def add_doctor():

    data = request.json

    if Doctor.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    doctor = Doctor(
        doctor_id=get_next_doctor_id(),
        name=data["name"],
        gender=data["gender"],
        mobile=data["mobile"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        specialization=data["specialization"],
        experience=data.get("experience", 0),
        schedule=data.get("schedule", ""),
        status="Active"
    )

    db.session.add(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor created successfully"}), 201

# ---------------------------------------------------------------------
@admin_bp.route("/admin/bulk-add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def bulk_add_doctor():

    data = request.json

    for i in data:
        if Doctor.query.filter_by(email=i["email"]).first():
            return jsonify({"error": "Email already exists"}), 400

        doctor = Doctor(
            doctor_id=get_next_doctor_id(),
            name=i["name"],
            gender=i["gender"],
            mobile=i["mobile"],
            email=i["email"],
            password=generate_password_hash(i["password"]),
            specialization=i["specialization"],
            experience=i.get("experience", 0),
            schedule=i.get("schedule", ""),
            status="Active"
        )
        db.session.add(doctor)

    db.session.commit()

    return jsonify({
        "message": "Doctors registered",
        "count": len(data)
    }), 201
# ---------------------------------------------------------------------





# -----------------------------
# Get All Doctors
# -----------------------------
@admin_bp.route("/admin/doctors", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_doctors():

    page = int(request.args.get("page", 1))
    per_page = 10
    search = request.args.get("search")

    query = Doctor.query
    if search:
        query = query.filter(db.or_(
            Doctor.name.ilike(f"%{search}%"),
            Doctor.doctor_id.ilike(f"%{search}%"),
            Doctor.specialization.ilike(f"%{search}%")
        ))
    
    pagination = query.order_by(Doctor.experience.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    doctors = []
    for d in pagination.items:
        doctors.append({
            "_id": str(d.id),
            "doctor_id": d.doctor_id,
            "name": d.name,
            "gender": d.gender,
            "mobile": d.mobile,
            "email": d.email,
            "specialization": d.specialization,
            "experience": d.experience,
            "schedule": d.schedule,
            "status": d.status,
            "image": d.image_url if d.image_url else f"https://ui-avatars.com/api/?name={d.name}"
        })

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "data": doctors
    })




# -----------------------------
# Fetch List of Doctor's Name
# -----------------------------
@admin_bp.route("/admin/doctors_name", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_doctors_name():
    doctors = Doctor.query.with_entities(Doctor.id, Doctor.name).all()

    result = []
    for d in doctors:
        result.append({
            "id": str(d.id),
            "name": d.name
        })

    return jsonify({
        "data": result
    })




# -----------------------------
# Update Doctor Status
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>/status", methods=["PUT"])
@jwt_required()
@role_required("Admin")
def update_doctor_status(doctor_id):

    data = request.json
    allowed_status = ["Active", "Inactive", "On Leave"]

    status = data.get("status")

    if not status or status not in allowed_status:
        return jsonify({"error": "Invalid status"}), 400

    if doctor_id.startswith("DOC-"):
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    else:
        doctor = Doctor.query.get(int(doctor_id))
    if doctor:
        doctor.status = status
        db.session.commit()
    else:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"message": "Status updated"})




# -----------------------------
# Update Doctor Profile
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["PUT"])
@jwt_required()
@role_required("Admin")
def update_doctor(doctor_id):

    data = request.json
    if doctor_id.startswith("DOC-"):
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    else:
        doctor = Doctor.query.get(int(doctor_id))

    if doctor:
        if "specialization" in data:
            doctor.specialization = data["specialization"]
        if "experience" in data:
            doctor.experience = data["experience"]
        if "schedule" in data:
            doctor.schedule = data["schedule"]
            
        db.session.commit()
    else:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"message": "Doctor updated"})




# -----------------------------
# Soft Delete Doctor
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["DELETE"])
@jwt_required()
@role_required("Admin")
def delete_doctor(doctor_id):
    
    if doctor_id.startswith("DOC-"):
        doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
    else:
        doctor = Doctor.query.get(int(doctor_id))
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
        
    doctor.status = "Inactive"
    db.session.commit()
    
    return jsonify({"message": "Doctor deactivated"})




#---------------------------------
# Get All Patients
# --------------------------------
@admin_bp.route("/admin/patients",methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_patients():

    page = int(request.args.get("page", 1))
    per_page = 10
    search = request.args.get("search")

    query = Patient.query
    if search:
        query = query.filter(db.or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.medical_id.ilike(f"%{search}%")
        ))
    
    pagination = query.order_by(Patient.medical_id.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    patients = []
    for p in pagination.items:
        patients.append({
            "_id": str(p.id),
            "medical_id": p.medical_id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "mobile": p.mobile,
            "email": p.email,
            "condition": p.condition,
            "admission_date": p.admission_date.strftime("%b %d, %Y") if p.admission_date else None,
            "last_visit": p.last_visit.strftime("%b %d, %Y") if p.last_visit else None
        })

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "data": patients
    })




#---------------------------------
# Get All Appointments
# --------------------------------
@admin_bp.route("/admin/appointments", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_appointments():

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search", type=str)
    doctor_id = request.args.get("doctor", type=str)
    start = request.args.get("start")
    end = request.args.get("end")

    query = Appointment.query.join(Patient).join(Doctor)

    if start and end:
        s_date = datetime.fromisoformat(start.replace("Z", ""))
        e_date = datetime.fromisoformat(end.replace("Z", ""))
        query = query.filter(Appointment.date >= s_date, Appointment.date <= e_date)
        
    if search:
        query = query.filter(db.or_(
            Patient.name.ilike(f"%{search}%"),
            Doctor.name.ilike(f"%{search}%")
        ))

    if doctor_id:
        query = query.filter(Appointment.doctor_id == int(doctor_id))

    pagination = query.order_by(Appointment.date.asc()).paginate(page=page, per_page=limit, error_out=False)
    
    appointments = []
    for a in pagination.items:
        appointments.append({
            "_id": str(a.id),
            "patient_id": str(a.patient_id),
            "doctor_id": str(a.doctor_id),
            "status": a.status,
            "date": a.date.strftime("%Y-%m-%d") if a.date else None,
            "time": a.date.strftime("%H:%M") if a.date else None,
            "patient_name": a.patient.name,
            "doctor_name": a.doctor.name,
            "department": a.doctor.specialization
        })

    return jsonify({
        "data": appointments,
        "total": pagination.total,
        "total_pages": pagination.pages
    })




# ---------------------------------
#  Appointment Trend
# ---------------------------------
@admin_bp.route("/admin/appointments-trend", methods=["GET"])
@jwt_required()
@role_required("Admin")
def appointment_trend():

    mode = request.args.get("range", "week")
    today = datetime.utcnow()
    
    if mode == "7days":
        start_date = today - timedelta(days=6)
    else:
        start_date = today - timedelta(days=today.weekday())

    appointments = Appointment.query.filter(Appointment.date >= start_date).all()
    
    days_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    counts = {v: 0 for k, v in days_map.items()}
    
    for a in appointments:
        if a.date:
            day_idx = a.date.weekday()
            counts[days_map[day_idx]] += 1
            
    data = []
    for day_idx in range(7):
        day_str = days_map[day_idx]
        data.append({
            "day": day_str,
            "visits": counts[day_str]
        })

    return jsonify(data)