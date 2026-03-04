from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from utils import role_required
from db import mongo

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin",methods=["GET"])
@jwt_required()
@role_required("Admin")
def stats():

    total = mongo.db.doctors.count_documents({})
    active = mongo.db.doctors.count_documents({"status": "Active"})
    inactive = mongo.db.doctors.count_documents({"status": "Inactive"})
    on_leave = mongo.db.doctors.count_documents({"status": "On Leave"})
    patients = mongo.db.patients.count_documents({})
    appointments = mongo.db.appointments.count_documents({})

    return jsonify({
        "total_doctors": total,
        "total_active_doctors": active,
        "total_inactive_doctors": inactive,
        "total_onleave_doctors": on_leave,
        "totsl_patients": patients,
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

    if mongo.db.doctors.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    doctor = {
        "name": data["name"],
        "gender": data["gender"],
        "mobile": data["mobile"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "specialization": data["specialization"],
        "experience": data.get("experience", 0),
        "schedule": data.get("schedule", ""),
        "status": "Active"
    }

    mongo.db.doctors.insert_one(doctor)

    return jsonify({"message": "Doctor created successfully"}), 201


@admin_bp.route("/admin/bulk-add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def bulk_add_doctor():

    data = request.json

    users = []

    for i in data:
            if mongo.db.doctors.find_one({"email": i["email"]}):
                return jsonify({"error": "Email already exists"}), 400

            doctor = {
                "name": i["name"],
                "gender": i["gender"],
                "mobile": i["mobile"],
                "email": i["email"],
                "password": generate_password_hash(i["password"]),
                "specialization": i["specialization"],
                "experience": i.get("experience", 0),
                "schedule": i.get("schedule", ""),
                "status": "Active"
            }

            users.append(doctor)

    mongo.db.doctors.insert_many(users)

    return jsonify({
        "message": "Doctors registered",
        "count": len(doctors)
    }), 201


# -----------------------------
# Get All Doctors
# -----------------------------
import math

@admin_bp.route("/admin/doctors", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_doctors():

    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page
    search = request.args.get("search")

    match_stage = {}

    if search:
        match_stage = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"specialization": {"$regex": search, "$options": "i"}}
            ]
        }

    pipeline = []

    if search:
        pipeline.append({"$match": match_stage})

    # Count total documents
    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.doctors.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page) if total else 0

    # Add pagination
    pipeline.append({"$sort": {"experience": -1}})
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": per_page})

    doctors = list(mongo.db.doctors.aggregate(pipeline))

    for d in doctors:
        d["_id"] = str(d["_id"])

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": doctors
    })


# -----------------------------
# See One Doctor
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_one_doctor(doctor_id):

    doctor = mongo.db.doctors.find_one({"_id": ObjectId(doctor_id)})

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    doctor["_id"] = str(doctor["_id"])

    return jsonify(doctor)


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