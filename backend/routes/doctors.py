from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from bson import ObjectId
from db import mongo
from datetime import datetime

doctor_bp = Blueprint("doctors", __name__)

# Doctor profile
@doctor_bp.route("/doctors/me", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_my_profile():
    user_id = get_jwt_identity()
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})

    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor["_id"] = str(doctor["_id"])
    return jsonify(doctor)


# todays dashboard
@doctor_bp.route("/doctor/dashboard", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def doctor_dashboard():

    doctor_id = get_jwt_identity()

    today = datetime.today().strftime("%Y-%m-%d")

    # Today's appointments
    today_appointments = list(
        mongo.db.appointments.find({
            "doctor_id": doctor_id,
            "date": today
        })
    )

    # Total patients for doctor
    total_patients = mongo.db.patients.count_documents({
        "doctor_id": doctor_id
    })

    # Pending reports
    pending_reports = mongo.db.reports.count_documents({
        "doctor_id": doctor_id,
        "status": "pending"
    })

    # Recent patients
    recent_patients = list(
        mongo.db.patients.find({"doctor_id": doctor_id})
        .sort("_id", -1)
        .limit(5)
    )

    for p in recent_patients:
        p["_id"] = str(p["_id"])

    for a in today_appointments:
        a["_id"] = str(a["_id"])

    return jsonify({
        "today_appointments": len(today_appointments),
        "appointments": today_appointments,
        "total_patients": total_patients,
        "pending_reports": pending_reports,
        "recent_patients": recent_patients
    })


# Doctor all appointments
@doctor_bp.route("/doctors/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def my_appointments():
    user_id = get_jwt_identity()
    appointments = list(mongo.db.appointments.find({"doctor_id": user_id}))

    for a in appointments:
        a["_id"] = str(a["_id"])

    return jsonify(appointments)


# patient condition update
@doctor_bp.route("/patients/<patient_id>/condition", methods=["PUT"])
@jwt_required()
@role_required("Doctor")
def update_condition(patient_id):

    data = request.json

    mongo.db.patients.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"condition": data["condition"]}}
    )

    return jsonify({"message": "Condition updated"})