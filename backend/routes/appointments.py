from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from db import mongo
from bson import ObjectId
from datetime import datetime

appointment_bp = Blueprint("appointments", __name__)


# ---------------------------------
# Patient books appointment
# ---------------------------------
@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
@role_required("Patient")
def create_appointment():
    user_id = get_jwt_identity()
    query_id = ObjectId(user_id) if isinstance(user_id, str) and len(user_id)==24 else user_id
    data = request.json
    
    try:
        date_str = data.get("date", "")
        if "T" in date_str:
            date_obj = datetime.strptime(date_str[:16], "%Y-%m-%dT%H:%M") # handles e.g. "2023-11-01T10:30"
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD or YYYY-MM-DDTHH:MM"}), 400

    appointment = {
        "patient_id": query_id,
        "doctor_id": ObjectId(data["doctor_id"]),
        "date": date_obj,
        "type": data.get("type", "Consultation"),
        "location": data.get("location", "Main Hospital"),
        "status": "Pending"
    }

    try:
        mongo.db.appointments.insert_one(appointment)
        mongo.db.patients.update_one(
            {"_id": query_id},
            {"$set": {"last_visit": appointment["date"]}}
        )
        return jsonify({"message": "Appointment booked safely"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------
# Admin view all appointments
# ---------------------------------
@appointment_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_appointments():

    appointments = list(mongo.db.appointments.find({}))

    for a in appointments:
        a["_id"] = str(a["_id"])
        a["patient_id"] = str(a["patient_id"])
        a["doctor_id"] = str(a["doctor_id"])

    return jsonify(appointments)


# ---------------------------------
# TEMP BULK APPOINTMENT INSERT
# ---------------------------------
from datetime import datetime
from bson import ObjectId

@appointment_bp.route("/appointments/bulk", methods=["POST"])
def bulk_appointments():

    data = request.json
    appointments = []

    for item in data:

        date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S")

        appointment = {
            "patient_id": ObjectId(item["patient_id"]),
            "doctor_id": ObjectId(item["doctor_id"]),
            "date": date,
            "status": "Scheduled"
        }

        appointments.append(appointment)

        # update patient's last visit
        mongo.db.patients.update_one(
            {"_id": ObjectId(item["patient_id"])},
            {"$set": {"last_visit": date}}
        )

    mongo.db.appointments.insert_many(appointments)

    return jsonify({"message": "Bulk appointments created"}), 201