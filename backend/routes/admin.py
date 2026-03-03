from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from utils import role_required
from db import mongo

admin_bp = Blueprint("admin", __name__)


# -----------------------------
# Add Doctor
# -----------------------------
@admin_bp.route("/admin/add-doctor", methods=["POST"])
@jwt_required()
@role_required("Admin")
def add_doctor():

    data = request.json

    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    client = mongo.cx

    with client.start_session() as session:
        with session.start_transaction():

            user = {
                "name": data["name"],
                "role": "Doctor",
                "gender": data["gender"],
                "mobile": data["mobile"],
                "email": data["email"],
                "password": generate_password_hash(data["password"])
            }

            user_result = mongo.db.users.insert_one(user, session=session)

            doctor_profile = {
                "user_id": user_result.inserted_id,
                "specialization": data["specialization"],
                "experience": data.get("experience", 0),
                "schedule": data.get("schedule", ""),
                "status": "Active"
            }

            mongo.db.doctors.insert_one(doctor_profile, session=session)

    return jsonify({"message": "Doctor created successfully"}), 201


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
                {"user.name": {"$regex": search, "$options": "i"}},
                {"specialization": {"$regex": search, "$options": "i"}}
            ]
        }

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

    if search:
        pipeline.append({"$match": match_stage})

    # Count total documents (for pagination info)
    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.doctors.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page)

    # Add pagination
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
# See One Doctor
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_one_doctor(doctor_id):

    pipeline = [
        {
            "$match": {
                "_id": ObjectId(doctor_id)
            }
        },
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

    doctor = list(mongo.db.doctors.aggregate(pipeline))

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    doctor = doctor[0]
    doctor["_id"] = str(doctor["_id"])
    doctor["user"]["_id"] = str(doctor["user"]["_id"])
    doctor["user_id"] = str(doctor["user_id"])

    return jsonify(doctor)


# -----------------------------
# Update Doctor Status
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>/status", methods=["PUT"])
@jwt_required()
@role_required("Admin")
def update_doctor_status(doctor_id):

    data = request.json
    allowed_status = ["Active", "Inactive", "On Leave"]

    if data["status"] not in allowed_status:
        return jsonify({"error": "Invalid status"}), 400

    mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"status": data["status"]}}
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

    mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {
            "specialization": data.get("specialization"),
            "experience": data.get("experience"),
            "schedule": data.get("schedule")
        }}
    )

    return jsonify({"message": "Doctor updated"})


# -----------------------------
# Soft Delete Doctor
# -----------------------------
@admin_bp.route("/admin/doctors/<doctor_id>", methods=["DELETE"])
@jwt_required()
@role_required("Admin")
def delete_doctor(doctor_id):

    mongo.db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"status": "Inactive"}}
    )

    return jsonify({"message": "Doctor deactivated"})