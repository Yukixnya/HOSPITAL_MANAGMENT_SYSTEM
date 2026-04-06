from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, or_
from utils import role_required, cache_delete_pattern, cache_get, cache_set
from extensions import db
from models import (
    Doctor,
    Patient,
    Appointment,
    MedicalRecord,
    Prescription,
    Note,
    Vital,
)
from datetime import date, datetime, timedelta


doctor_bp = Blueprint("doctors", __name__)


# -----------------------------
# Doctor Profile
# -----------------------------
@doctor_bp.route("/doctors/me", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_my_profile():
    user_id = int(get_jwt_identity())

    cache_key = f"doctor:profile:{user_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(cached), 200

    doctor = Doctor.query.get(user_id)
    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    data = {
        "_id": str(doctor.id),
        "doctor_id": doctor.doctor_id,
        "name": doctor.name,
        "email": doctor.email,
        "specialization": doctor.specialization,
        "experience": doctor.experience,
        "schedule": doctor.schedule,
        "status": doctor.status,
        "mobile": doctor.mobile,
        "gender": doctor.gender,
        "image": doctor.image_url or f"https://ui-avatars.com/api/?name={doctor.name}",
    }

    cache_set(cache_key, data, ttl=300)

    return jsonify(data), 200


# Todays dashboard
@doctor_bp.route("/doctors/dashboard", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def doctor_dashboard():
    doctor_id = int(get_jwt_identity())

    # For today filtering, start and end of day datetime objects
    now = datetime.utcnow()
    start_of_today = datetime(now.year, now.month, now.day)

    # Weekly schedule from Monday (0) to Sunday (6) of current week
    start_of_week = start_of_today - timedelta(days=start_of_today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    cache_key = (
        f"doctor:dashboard:{doctor_id}:{start_of_week.date()}:{end_of_week.date()}"
    )
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200

    # 1. Weekly appointments
    appointments = (
        Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != "Cancelled",
            Appointment.date >= start_of_week,
            Appointment.date < end_of_week,
        )
        .order_by(Appointment.date.asc())
        .all()
    )

    weekly_schedule = []
    for appt in appointments:
        if appt.patient:
            weekly_schedule.append(
                {
                    "_id": str(appt.id),
                    "patient_id": str(appt.patient_id),
                    "doctor_id": str(appt.doctor_id),
                    "status": appt.status,
                    "type": appt.type if appt.type else "Consultation",
                    "date": appt.date.strftime("%Y-%m-%d") if appt.date else "",
                    "time": appt.date.strftime("%H:%M") if appt.date else "",
                    "patient_name": appt.patient.name,
                    "patient_age": appt.patient.age,
                    "patient_gender": appt.patient.gender,
                }
            )

    today_str = start_of_today.strftime("%Y-%m-%d")
    today_appointments = [
        appt for appt in weekly_schedule if appt.get("date") == today_str
    ]

    # 2. Total patients count
    total_patients = Patient.query.count()

    # 3. Pending reports count
    # pending_reports = MedicalRecord.query.filter_by(doctor_id=doctor_id, status="Pending").count()

    # 4. Recent patients
    recent = (
        Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "Completed",
            Appointment.date == start_of_today,
        )
        .order_by(Appointment.date.desc())
        .limit(5)
        .all()
    )

    recent_patients = []
    for appt in recent:
        if appt.patient:
            recent_patients.append(
                {
                    "_id": str(appt.patient.id),
                    "medical_id": appt.patient.medical_id,
                    "name": appt.patient.name,
                    "age": appt.patient.age,
                }
            )

    data = {
        "today_appointments": len(today_appointments),
        "appointments": today_appointments,
        "weekly_schedule": weekly_schedule,
        "total_patients": total_patients,
        # "pending_reports": pending_reports,
        "recent_patients": recent_patients,
    }

    cache_set(cache_key, json.dumps(data), ttl=300)

    return jsonify(data), 200


# -----------------------------
# Doctor All Appointments
# -----------------------------
@doctor_bp.route("/doctors/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def my_appointments():
    doctor_id = int(get_jwt_identity())

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Filters
    search = request.args.get("search", type=str)
    status = request.args.get("status", type=str)

    cache_key = f"doctor:{doctor_id}:appointments:{page}:{search}:{status}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200

    # Base query
    query = Appointment.query.join(Patient).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status != "Completed",
        Appointment.status != "Cancelled",
    )

    # Status filtering
    if status == "Today":
        today_str = date.today().strftime("%Y-%m-%d")
        query = query.filter(func.date(Appointment.date) == today_str)
    elif status:
        query = query.filter(Appointment.status == status)

    # Search filtering
    if search:
        query = query.filter(
            or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.medical_id.ilike(f"%{search}%"),
            )
        )

    # Pagination & ordering
    pagination = query.order_by(Appointment.date.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Format response
    formatted_appointments = [
        {
            "_id": str(appt.id),
            "patient_id": str(appt.patient_id),
            "doctor_id": str(appt.doctor_id),
            "status": appt.status,
            "type": appt.type if appt.type else "Consultation",
            "date": appt.date.strftime("%Y-%m-%d") if appt.date else "",
            "time": appt.date.strftime("%H:%M") if appt.date else "",
            "patient_name": appt.patient.name,
            "patient_age": appt.patient.age,
            "patient_gender": appt.patient.gender,
            "medical_id": appt.patient.medical_id,
        }
        for appt in pagination.items
    ]

    data = {
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
        },
        "data": formatted_appointments,
    }

    cache_set(cache_key, json.dumps(data), ttl=300)

    return jsonify(data), 200


# -----------------------------
# Doctor All Patients
# -----------------------------
@doctor_bp.route("/doctors/patients", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_patients():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    search = request.args.get("search")
    patient_filter = request.args.get("filter")

    cache_key = f"doctor:{doctor_id}:patients:{page}:{search}:{patient_filter}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200

    query = Patient.query
    if patient_filter and patient_filter != "All Patients":
        query = query.filter(Patient.condition == patient_filter)
    if search:
        query = query.filter(
            db.or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.medical_id.ilike(f"%{search}%"),
                Patient.condition.ilike(f"%{search}%"),
            )
        )

    query = query.filter()

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    patients = []
    for p in pagination.items:
        patients.append(
            {
                "_id": str(p.id),
                "medical_id": p.medical_id,
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "condition": p.condition,
                "email": p.email,
                "mobile": p.mobile,
                "last_visit": (
                    p.last_visit.strftime("%Y-%m-%d") if p.last_visit else None
                ),
                "admission_date": (
                    p.admission_date.strftime("%Y-%m-%d") if p.admission_date else None
                ),
            }
        )

    data = {
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
        },
        "data": patients,
    }

    cache_set(cache_key, json.dumps(data), ttl=60)

    return jsonify(data), 200


# -----------------------------
# Single Patient Profile
# -----------------------------
@doctor_bp.route("/doctors/patient-profile/<patient_id>", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def patient_profile(patient_id):
    if patient_id.startswith("MR-"):
        patient = Patient.query.filter_by(medical_id=patient_id).first()
    else:
        patient = Patient.query.get(int(patient_id))
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    cache_key = f"doctor:patient:{patient_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200

    bp_vital = (
        Vital.query.filter_by(patient_id=patient.id, label="Blood Pressure")
        .order_by(Vital.id.desc())
        .first()
    )
    hr_vital = (
        Vital.query.filter_by(patient_id=patient.id, label="Heart Rate")
        .order_by(Vital.id.desc())
        .first()
    )

    blood_pressure_str = (
        f"{bp_vital.value} {bp_vital.unit or ''}".strip() if bp_vital else None
    )
    heart_rate_str = (
        f"{hr_vital.value} {hr_vital.unit or ''}".strip() if hr_vital else None
    )

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    appt_ids = [apt.id for apt in appointments]
    prescriptions = []
    if appt_ids:
        prescs = (
            Prescription.query.filter(Prescription.appointment_id.in_(appt_ids))
            .order_by(Prescription.id.desc())
            .all()
        )
        for pr in prescs:
            prescriptions.append(
                {
                    "name": pr.name,
                    "dosage": pr.dosage,
                    "frequency": pr.frequency,
                    "duration": pr.duration,
                }
            )

    all_records = (
        MedicalRecord.query.filter_by(patient_id=patient.id)
        .order_by(MedicalRecord.date.desc(), MedicalRecord.id.desc())
        .all()
    )
    medical_records = [
        {
            "id": mr.id,
            "date": mr.date,
            "title": mr.title,
            "description": mr.description,
            "appointment_id": mr.appointment_id,
        }
        for mr in all_records
    ]

    data = {
        "_id": str(patient.id),
        "medical_id": patient.medical_id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "condition": patient.condition,
        "last_visit": patient.last_visit.isoformat() if patient.last_visit else None,
        "admission_date": (
            patient.admission_date.isoformat() if patient.admission_date else None
        ),
        "dob": patient.dob,
        "blood_type": patient.blood_type,
        "blood_pressure": blood_pressure_str,
        "heart_rate": heart_rate_str,
        "prescriptions": prescriptions,
        "recent_medical_records": medical_records,
    }

    cache_set(cache_key, json.dumps(data), ttl=300)

    return jsonify(data), 200


# -----------------------------
# Patient Condition Update
# -----------------------------
@doctor_bp.route("/patients/<patient_id>/condition", methods=["PUT"])
@jwt_required()
@role_required("Doctor")
def update_condition(patient_id):
    if patient_id.startswith("MR-"):
        patient = Patient.query.filter_by(medical_id=patient_id).first()
    else:
        patient = Patient.query.get(int(patient_id))
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.json
    patient.condition = data.get("condition", "")
    db.session.commit()
    cache_delete_pattern(f"doctor:{doct}")
    return jsonify(
        {"message": "Patient condition updated"},
    )


# -----------------------------
# Add Prescription
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/prescription", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_prescription(apt_id):

    apt = Appointment.query.get(int(apt_id))
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected array"}), 400

    created = []

    for item in data:
        if not all(
            [
                item.get("name"),
                item.get("dosage"),
                item.get("frequency"),
                item.get("duration"),
            ]
        ):
            return jsonify({"error": "All fields required"}), 400

        p = Prescription(
            appointment_id=apt.id,
            patient_id=apt.patient_id,
            name=item["name"],
            dosage=item["dosage"],
            frequency=item["frequency"],
            duration=item["duration"],
        )
        db.session.add(p)
        created.append(p)

    db.session.commit()

    cache_delete_pattern("doctor:*")

    return (
        jsonify({"message": "Prescription added", "ids": [p.id for p in created]}),
        201,
    )


# -----------------------------
# Add Note
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/note", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_note(apt_id):

    apt = Appointment.query.get(int(apt_id))
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()

    if not data.get("text"):
        return jsonify({"error": "Note text required"}), 400

    n = Note(
        appointment_id=apt.id,
        patient_id=apt.patient_id,
        text=data["text"],
        date=datetime.utcnow().isoformat(),
    )

    db.session.add(n)
    db.session.commit()

    cache_delete_pattern("doctor:*")

    return jsonify({"id": n.id}), 201


# -----------------------------
# Add Vital
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/vital", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_vital(apt_id):

    apt = Appointment.query.get(int(apt_id))
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected array of vitals"}), 400

    created = []

    for item in data:
        if not item.get("label") or not item.get("value"):
            return jsonify({"error": "label and value required"}), 400

        v = Vital(
            appointment_id=apt.id,
            patient_id=apt.patient_id,
            label=item["label"],
            value=item["value"],
            unit=item.get("unit"),
        )
        db.session.add(v)
        created.append(v)

    db.session.commit()

    cache_delete_pattern("doctor:*")

    return jsonify({"message": "Vitals added", "ids": [v.id for v in created]}), 201


# -----------------------------
# Add Medical Record (Unified History/Timeline API)
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/medical-record", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_medical_record(apt_id):

    apt = Appointment.query.get(int(apt_id))
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    doctor_id = int(get_jwt_identity())

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    record = MedicalRecord.query.filter_by(appointment_id=apt.id).first()

    if not record:
        record = MedicalRecord(
            patient_id=apt.patient_id,
            doctor_id=doctor_id,
            appointment_id=apt.id,
            date=datetime.utcnow(),
            title=data.get("title"),
            description=data.get("description"),
        )
        db.session.add(record)
        db.session.commit()
        status_code = 201
    else:
        record.title = data.get("title")
        record.description = data.get("description")
        status_code = 200

    # --- LINK ARRAYS ---
    for vid in data.get("vital_ids", []):
        v = Vital.query.get(vid)
        if not v or v.appointment_id != apt.id:
            return jsonify({"error": f"Invalid vital_id {vid}"}), 400
        v.medical_record_id = record.id

    for nid in data.get("note_ids", []):
        n = Note.query.get(nid)
        if not n:
            return jsonify({"error": f"Invalid note_id {nid}"}), 400
        n.medical_record_id = record.id

    for pid in data.get("prescription_ids", []):
        p = Prescription.query.get(pid)
        if not p:
            return jsonify({"error": f"Invalid prescription_id {pid}"}), 400
        p.medical_record_id = record.id

    apt.status = "Completed"

    db.session.commit()

    cache_delete_pattern("doctor:*")
    cache_delete_pattern("appointments:*")

    return (
        jsonify({"message": "Medical record saved", "record_id": record.id}),
        status_code,
    )
