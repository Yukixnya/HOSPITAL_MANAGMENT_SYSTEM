from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from utils import role_required
from datetime import datetime, timedelta
from db import mongo

from services.admin.dashboard import stat_data
from HOSPITAL_MANAGMENT_SYSTEM.backend.services.admin.doctor_service import add_one_doctor , add_many_doctor
from services.admin.get_service import all_doctors,all_patients,all_appointments


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin",methods=["GET"])
@jwt_required()
@role_required("Admin")
def stats():
    data = stat_data()
    return jsonify(data),200

# -----------------------------
# Add Doctor
# -----------------------------
@admin_bp.route("/admin/add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def add_doctor():

    data = request.json
    result, status = add_one_doctor(data)

    return jsonify(result), status

@admin_bp.route("/admin/bulk-add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def bulk_add_doctor():

    data = request.json
    result,status = add_many_doctor(data)

    return jsonify(result),status


# -----------------------------
# Get All Doctors
# -----------------------------
@admin_bp.route("/admin/doctors", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_doctors():

    page = int(request.args.get("page", 1))
    search = request.args.get("search")

    result, status = all_doctors(page, search)

    return jsonify(result), status


# --------------------------------------------------
# Filters
# --------------------------------------------------
@admin_bp.route("/admin/doctors-filter", methods=["GET"])
@jwt_required()
@role_required("Admin")
def filter():


    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page

    search = request.args.get("search")
    status = request.args.get("status")
    specialization = request.args.get("specialization")
    min_exp = request.args.get("min_exp")

    match_conditions = []

    # Search Filter
    if search:
        match_conditions.append({
            "$or": [
                {"user.name": {"$regex": search, "$options": "i"}},
                {"specialization": {"$regex": search, "$options": "i"}}
            ]
        })

    # Status Filter
    if status:
        match_conditions.append({"status": status})

    # Specialization Filter
    if specialization:
        match_conditions.append({"specialization": specialization})

    # Minimum Experience Filter
    if min_exp:
        match_conditions.append({"experience": {"$gte": int(min_exp)}})

    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {"$unwind": "$user"}
    ]

    # Apply filters if any
    if match_conditions:
        pipeline.append({
            "$match": {
                "$and": match_conditions
            }
        })


    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.doctors.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page) if total else 0


    pipeline.append({"$sort": {"experience": -1}})

    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": per_page})
    pipeline.append({"$project": {"password": 0}})

    doctors = list(mongo.db.doctors.aggregate(pipeline))

    for d in doctors:
        d["_id"] = str(d["_id"])
        d["user"]["_id"] = str(d["user"]["_id"])
        d["user_id"] = str(d["user_id"])

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": doctors
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

    mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"status": status}}
    )

    return jsonify({"message": "Status updated"})


# -----------------------------
# Update Doctor Profile
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["PUT"])
@jwt_required()
@role_required("Admin")
def update_doctor(doctor_id):

    data = request.json

    update_fields = {}

    if "specialization" in data:
        update_fields["specialization"] = data["specialization"]

    if "experience" in data:
        update_fields["experience"] = data["experience"]

    if "schedule" in data:
        update_fields["schedule"] = data["schedule"]

    mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": update_fields}
    )

    return jsonify({"message": "Doctor updated"})


# -----------------------------
# Soft Delete Doctor
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["DELETE"])
@jwt_required()
@role_required("Admin")
def delete_doctor(doctor_id):

    result = mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"status": "Inactive"}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({"message": "Doctor deactivated"})


#---------------------------------
# Get All Patients
# --------------------------------
@admin_bp.route("/admin/patients",methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_patients():

    page = int(request.args.get("page", 1))
    search = request.args.get("search")

    result, status = all_patients(page, search)

    return jsonify(result), status

# -----------------------------
# Get All Appointments
# -----------------------------
@admin_bp.route("/admin/appointments", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_appointments():

    page = int(request.args.get("page", 1))
    search = request.args.get("search")

    result, status = all_appointments(page, search)

    return jsonify(result), status

#---------------------------------
# Appointment Trend
#---------------------------------
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

    pipeline = [
        {
            "$match": {
                "date": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": {"$dayOfWeek": "$date"},
                "visits": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "day": "$_id",
                "visits": 1
            }
        },
        {"$sort": {"day": 1}}
    ]

    data = list(mongo.db.appointments.aggregate(pipeline))

    days_map = {
        1: "Sun",
        2: "Mon",
        3: "Tue",
        4: "Wed",
        5: "Thu",
        6: "Fri",
        7: "Sat"
    }

    for d in data:
        d["day"] = days_map[d["day"]]

    return jsonify(data)