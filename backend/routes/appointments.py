from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from extensions import db
from models import Appointment, Patient, Doctor
from datetime import datetime

appointment_bp = Blueprint("appointments", __name__)




# ---------------------------------
# Patient books appointment
# ---------------------------------
@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
@role_required("Patient")
def create_appointment():
    user_id = int(get_jwt_identity())
    data = request.json
    
    try:
        date_str = data.get("date", "")
        if "T" in date_str:
            date_obj = datetime.strptime(date_str[:16], "%Y-%m-%dT%H:%M") # handles e.g. "2023-11-01T10:30"
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD or YYYY-MM-DDTHH:MM"}), 400

    appointment = Appointment(
        patient_id=user_id,
        doctor_id=int(data["doctor_id"]),
        date=date_obj,
        type=data.get("type", "Consultation"),
        location=data.get("location", "Main Hospital"),
        status="Pending",
        diagnosisTitle="Pending Assessment",
        diagnosisCode="-",
        diagnosisDesc="Awaiting official notes."
    )

    try:
        db.session.add(appointment)
        patient = Patient.query.get(user_id)
        if patient:
            patient.last_visit = date_obj
        db.session.commit()
        return jsonify({"message": "Appointment booked safely"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




# ---------------------------------
# TEMP BULK APPOINTMENT INSERT
# ---------------------------------
@appointment_bp.route("/appointments/bulk", methods=["POST"])
def bulk_appointments():

    data = request.json

    for item in data:

        date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S")
        patient_id = int(item["patient_id"])
        doctor_id = int(item["doctor_id"])

        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            status="Scheduled",
            type="Consultation",
            diagnosisTitle="Pending Assessment",
            diagnosisCode="-",
            diagnosisDesc="Awaiting official notes."
        )

        db.session.add(appointment)

        patient = Patient.query.get(patient_id)
        if patient:
            patient.last_visit = date

    db.session.commit()

    return jsonify({"message": "Bulk appointments created"}), 201