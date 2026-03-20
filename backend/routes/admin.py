from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from utils import role_required
from datetime import datetime, timedelta
from db import mongo
import math

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

    print("data from frontend", data)

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

# ---------------------------------------------------------------------
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
# ---------------------------------------------------------------------

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
    pipeline.append({"$project": {"password": 0}})

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


# # -----------------------------
# # Fetch List of Doctor's Name
# # -----------------------------
@admin_bp.route("/admin/doctors_name", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_doctors_name():
    doctors = mongo.db.doctors.find({}, {"name": 1})

    result = []
    for d in doctors:
        result.append({
            "id": str(d["_id"]),
            "name": d["name"]
        })

    return jsonify({
        "data": result
    })

# # -----------------------------
# # See One Doctor
# # -----------------------------
# @admin_bp.route("/admin/doctors/<doctor_id>", methods=["GET"])
# @jwt_required()
# @role_required("Admin")
# def get_one_doctor(doctor_id):

#     doctor = mongo.db.doctors.find_one({"_id": ObjectId(doctor_id)})

#     if not doctor:
#         return jsonify({"error": "Doctor not found"}), 404

#     doctor["_id"] = str(doctor["_id"])

#     return jsonify(doctor)


# --------------------------------------------------
# Filters
# --------------------------------------------------
@admin_bp.route("/admin/doctors-filter", methods=["GET"])
@jwt_required()
@role_required("Admin")
def filter_doctors():

    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page

    search = request.args.get("search")
    status = request.args.get("status")
    specialization = request.args.get("specialization")
    min_exp = request.args.get("min_exp")

    query = {}

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"specialization": {"$regex": search, "$options": "i"}}
        ]

    if status:
        query["status"] = status

    if specialization:
        query["specialization"] = specialization

    if min_exp:
        query["experience"] = {"$gte": int(min_exp)}

    total = mongo.db.doctors.count_documents(query)

    doctors = list(
        mongo.db.doctors
        .find(query, {"password": 0})
        .sort("experience", -1)
        .skip(skip)
        .limit(per_page)
    )

    for d in doctors:
        d["_id"] = str(d["_id"])

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": math.ceil(total / per_page),
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
    per_page = 10
    skip = (page - 1) * per_page
    search = request.args.get("search")

    match_stage = {}

    if search:
        match_stage = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"medical_id":{"$regex":search,"$options":"i"}}
            ]
        }

    pipeline = []

    if search:
        pipeline.append({"$match": match_stage})

    # Count total documents
    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.patients.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page) if total else 0

    # Add pagination
    pipeline.append({"$sort": {"medical_id": 1}})
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": per_page})
    pipeline.append({"$project": {"password": 0}})

    patients = list(mongo.db.patients.aggregate(pipeline))

    for p in patients:
        p["_id"] = str(p["_id"])
        if p.get("admission_date"):
            p["admission_date"] = p["admission_date"].strftime("%b %d, %Y")

        if p.get("last_visit"):
            p["last_visit"] = p["last_visit"].strftime("%b %d, %Y")

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
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
    doctor = request.args.get("doctor", type=str)

    start = request.args.get("start")
    end = request.args.get("end")

    pipeline = []
    match_query = {}

    # Date filter
    if start and end:
        match_query["date"] = {
            "$gte": datetime.fromisoformat(start.replace("Z", "")),
            "$lte": datetime.fromisoformat(end.replace("Z", ""))
        }

    if match_query:
        pipeline.append({"$match": match_query})

    # Join patients
    pipeline.append({
        "$lookup": {
            "from": "patients",
            "localField": "patient_id",
            "foreignField": "_id",
            "as": "patient_info"
        }
    })

    # Join doctors
    pipeline.append({
        "$lookup": {
            "from": "doctors",
            "localField": "doctor_id",
            "foreignField": "_id",
            "as": "doctor_info"
        }
    })

    # Flatten arrays
    pipeline.append({
        "$unwind": {"path": "$patient_info", "preserveNullAndEmptyArrays": True}
    })

    pipeline.append({
        "$unwind": {"path": "$doctor_info", "preserveNullAndEmptyArrays": True}
    })

    # Search filter
    if search:
        pipeline.append({
            "$match": {
                "$or": [
                    {"patient_info.name": {"$regex": search, "$options": "i"}},
                    {"doctor_info.name": {"$regex": search, "$options": "i"}},
                ]
            }
        })

    # Doctor filter
    if doctor:
        pipeline.append({
            "$match": {
                "doctor_info._id": ObjectId(doctor)
            }
        })

    # Count pipeline
    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.appointments.aggregate(count_pipeline))
    total = count_result[0]["total"] if count_result else 0

    # Pagination
    skip = (page - 1) * limit
    pipeline.append({"$sort": {"date": 1}})
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": limit})

    # Final projection
    pipeline.append({
        "$project": {
            "_id": {"$toString": "$_id"},
            "patient_id": {"$toString": "$patient_id"},
            "doctor_id": {"$toString": "$doctor_id"},
            "status": 1,
            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            "time": {"$dateToString": {"format": "%H:%M", "date": "$date"}},
            "patient_name": "$patient_info.name",
            "doctor_name": "$doctor_info.name",
            "department": "$doctor_info.specialization"
        }
    })

    appointments = list(mongo.db.appointments.aggregate(pipeline))

    return jsonify({
        "data": appointments,
        "total": total,
        "total_pages": math.ceil(total / limit) if limit else 1
    })

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