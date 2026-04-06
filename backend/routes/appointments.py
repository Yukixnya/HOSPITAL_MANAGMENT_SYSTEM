from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required, get_next_appointment_id, cache_delete_pattern
from extensions import db
from models import Appointment, Patient, Doctor
from datetime import datetime
from sqlalchemy.orm import joinedload

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
            date_obj = datetime.strptime(date_str[:16], "%Y-%m-%dT%H:%M")
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return (
            jsonify(
                {
                    "error": "Invalid date format, expected YYYY-MM-DD or YYYY-MM-DDTHH:MM"
                }
            ),
            400,
        )

    appointment = Appointment(
        patient_id=user_id,
        doctor_id=int(data["doctor_id"]),
        date=date_obj,
        type=data.get("type", "Consultation"),
        status="Pending",
        diagnosisTitle="Pending Assessment",
        diagnosisDesc="Awaiting official notes.",
    )

    try:
        db.session.add(appointment)
        patient = Patient.query.get(user_id)
        if patient:
            patient.last_visit = date_obj
        db.session.commit()

        cache_delete_pattern("admin:appointments:*")
        cache_delete_pattern("patient:appointments:*")
        cache_delete_pattern("doctors:*")

        return jsonify({"message": "Appointment booked safely"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Patient reschedule appointment
# -------------------------------
@appointment_bp.route(
    "/patients/appointments/<string:appointment_id>/reschedule", methods=["PATCH"]
)
@jwt_required()
@role_required("Patient")
def reschedule_appointment(appointment_id):
    user_id = int(get_jwt_identity())
    data = request.json or {}

    try:
        date_str = data.get("date", "")
        if "T" in date_str:
            date_obj = datetime.strptime(
                date_str[:16], "%Y-%m-%dT%H:%M"
            )  # handles e.g. "2023-11-01T10:30"
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return (
            jsonify(
                {
                    "error": "Invalid date format, expected YYYY-MM-DD or YYYY-MM-DDTHH:MM"
                }
            ),
            400,
        )

    appointment = Appointment.query.filter_by(
        id=appointment_id, patient_id=user_id
    ).first()

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status == "Cancelled":
        return (
            jsonify({"error": "Appointment cannot be rescheduled as it is cancelled"}),
            400,
        )

    try:
        appointment.date = date_obj
        if "type" in data:
            appointment.type = data["type"]

        patient = Patient.query.get(user_id)
        if patient:
            patient.last_visit = date_obj

        db.session.commit()
        cache_delete_pattern("admin:appointments:*")
        cache_delete_pattern("patient:appointments:*")
        return jsonify({"message": "Appointment rescheduled successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------------
# Patient cancel appointment
# ---------------------------------
@appointment_bp.route(
    "/patients/appointments/<string:appointment_id>/cancel", methods=["DELETE"]
)
@jwt_required()
@role_required("Patient")
def cancel_appointment(appointment_id):
    user_id = int(get_jwt_identity())

    try:
        appointment = Appointment.query.filter_by(
            id=appointment_id, patient_id=user_id
        ).first()
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        if appointment.status == "Cancelled":
            return jsonify({"error": "Appointment already cancelled"}), 400
        appointment.status = "Cancelled"
        db.session.commit()
        cache_delete_pattern("admin:appointments:*")
        cache_delete_pattern("patient:appointments:*")
        return jsonify({"message": "Appointment cancelled successfully"}), 200
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
            appointment_id=get_next_appointment_id(),
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            status="Scheduled",
            type="Consultation",
            diagnosisTitle="Pending Assessment",
            diagnosisDesc="Awaiting official notes.",
        )

        db.session.add(appointment)

        patient = Patient.query.get(patient_id)
        if patient:
            patient.last_visit = date

    db.session.commit()

    return jsonify({"message": "Bulk appointments created"}), 201


# ---------------------------------
# Doctor confirm appointment
# ---------------------------------
@appointment_bp.route(
    "/doctors/appointments/<string:appointment_id>/confirm", methods=["PATCH"]
)
@jwt_required()
@role_required("Doctor")
def confirm_appointment(appointment_id):
    doctor_id = int(get_jwt_identity())

    appointment = Appointment.query.filter_by(
        id=appointment_id, doctor_id=doctor_id
    ).first()

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status != "Pending":
        return jsonify({"error": "Only pending appointments can be confirmed"}), 400

    try:
        appointment.status = "Confirmed"
        db.session.commit()
        cache_delete_pattern("admin:appointments:*")
        cache_delete_pattern(f"doctor:{doctor_id}:appointments:*")
        cache_delete_pattern(f"patient:{appointment.patient_id}:appointments:*")
        return jsonify({"message": "Appointment confirmed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------------
# Doctor cancel appointment
# ---------------------------------
@appointment_bp.route(
    "/doctors/appointments/<string:appointment_id>/cancel", methods=["PATCH"]
)
@jwt_required()
@role_required("Doctor")
def cancel_appointment_doctor(appointment_id):
    doctor_id = int(get_jwt_identity())

    appointment = Appointment.query.filter_by(
        id=appointment_id, doctor_id=doctor_id
    ).first()

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    if appointment.status != "Pending" and appointment.status != "Confirmed":
        return jsonify({"error": "Only pending appointments can be cancelled"}), 400

    try:
        appointment.status = "Cancelled"
        db.session.commit()
        cache_delete_pattern("admin:appointments:*")
        cache_delete_pattern(f"doctor:{doctor_id}:appointments:*")
        cache_delete_pattern(f"patient:{appointment.patient_id}:appointments:*")
        return jsonify({"message": "Appointment cancelled successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------------
# Doctor get a specific appointment
# ---------------------------------
@appointment_bp.route("/doctors/appointments/<string:appointment_id>", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_appointment_status(appointment_id):
    user_id = int(get_jwt_identity())

    try:
        appointment = (
            Appointment.query.options(joinedload(Appointment.patient))
            .filter_by(id=appointment_id)
            .first()
        )

        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        if appointment.patient_id != user_id and appointment.doctor_id != user_id:
            return jsonify({"error": "Unauthorized access to appointment status"}), 403

        appointment_data = {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "date": appointment.date.isoformat() if appointment.date else None,
            "patient": {
                "id": appointment.patient.id,
                "name": appointment.patient.name,
                "age": appointment.patient.age,
                "gender": appointment.patient.gender,
                "medical_id": appointment.patient.medical_id,
            },
        }

        return jsonify(data=appointment_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
