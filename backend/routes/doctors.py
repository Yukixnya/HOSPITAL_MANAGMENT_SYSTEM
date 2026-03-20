from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from bson import ObjectId
from db import mongo
from datetime import datetime, timedelta

doctor_bp = Blueprint("doctors", __name__)

# Doctor profile
@doctor_bp.route("/doctors/me", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_my_profile():
    user_id = get_jwt_identity()
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)}, {"password": 0})

    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor["_id"] = str(doctor["_id"])
    return jsonify(doctor)


# Todays dashboard
@doctor_bp.route("/doctor/dashboard", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def doctor_dashboard():
    doctor_id = get_jwt_identity()
    query_id = ObjectId(doctor_id) if isinstance(doctor_id, str) and len(doctor_id)==24 else doctor_id

    # For today filtering, start and end of day datetime objects
    now = datetime.utcnow()
    start_of_today = datetime(now.year, now.month, now.day)
    
    # Weekly schedule from Monday (0) to Sunday (6) of current week
    start_of_week = start_of_today - timedelta(days=start_of_today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    # 1. Weekly appointments
    pipeline_week = [
        {"$match": {
            "doctor_id": query_id,
            "date": {"$gte": start_of_week, "$lt": end_of_week}
        }},
        {"$lookup": {
            "from": "patients",
            "localField": "patient_id",
            "foreignField": "_id",
            "as": "patient_info"
        }},
        {"$unwind": {"path": "$patient_info", "preserveNullAndEmptyArrays": True}},
        {"$sort": {"date": 1}},
        {"$project": {
            "_id": {"$toString": "$_id"},
            "patient_id": {"$toString": "$patient_id"},
            "doctor_id": {"$toString": "$doctor_id"},
            "status": 1,
            "type": {"$ifNull": ["$type", "Consultation"]},
            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            "time": {"$dateToString": {"format": "%H:%M", "date": "$date"}},
            "patient_name": "$patient_info.name",
            "patient_age": "$patient_info.age",
            "patient_gender": "$patient_info.gender"
        }}
    ]
    weekly_schedule = list(mongo.db.appointments.aggregate(pipeline_week))
    
    today_str = start_of_today.strftime("%Y-%m-%d")
    today_appointments = [appt for appt in weekly_schedule if appt.get("date") == today_str]

    # 2. Total patients count
    total_patients = mongo.db.patients.count_documents({})

    # 3. Pending reports count (checking the newly seeded medical_records)
    pending_reports = 0
    if "medical_records" in mongo.db.list_collection_names():
        pending_reports = mongo.db.medical_records.count_documents({"doctor_id": query_id, "status": "Pending"})

    # 4. Recent patients
    recent_patients_cursor = mongo.db.patients.find().sort("_id", -1).limit(5)
    recent_patients = []
    for p in recent_patients_cursor:
        recent_patients.append({
            "_id": str(p["_id"]),
            "medical_id": p.get("medical_id"),
            "name": p.get("name"),
            "gender": p.get("gender"),
            "age": p.get("age")
        })

    return jsonify({
        "today_appointments": len(today_appointments),
        "appointments": today_appointments,
        "weekly_schedule": weekly_schedule,
        "total_patients": total_patients,
        "pending_reports": pending_reports,
        "recent_patients": recent_patients
    })


# Doctor all appointments
@doctor_bp.route("/doctors/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def my_appointments():
    doctor_id = get_jwt_identity()
    query_id = ObjectId(doctor_id) if isinstance(doctor_id, str) and len(doctor_id)==24 else doctor_id

    page = request.args.get('page', 1, type=int)
    per_page = 10
    skip = (page - 1) * per_page
    
    search = request.args.get("search")
    status = request.args.get("status")

    match_query = {"doctor_id": query_id}
    if status:
        match_query["status"] = status

    pipeline = [
        {"$match": match_query},
        {"$lookup": {
            "from": "patients",
            "localField": "patient_id",
            "foreignField": "_id",
            "as": "patient_info"
        }},
        {"$unwind": {"path": "$patient_info", "preserveNullAndEmptyArrays": True}}
    ]

    if search:
        pipeline.append({
            "$match": {
                "$or": [
                    {"patient_info.name": {"$regex": search, "$options": "i"}},
                    {"patient_info.medical_id": {"$regex": search, "$options": "i"}}
                ]
            }
        })

    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.appointments.aggregate(count_pipeline))
    total_items = count_result[0]["total"] if count_result else 0
    total_pages = (total_items + per_page - 1) // per_page if per_page else 0

    pipeline.extend([
        {"$sort": {"date": 1}},
        {"$skip": skip},
        {"$limit": per_page},
        {"$project": {
            "_id": {"$toString": "$_id"},
            "patient_id": {"$toString": "$patient_id"},
            "doctor_id": {"$toString": "$doctor_id"},
            "status": 1,
            "type": {"$ifNull": ["$type", "Consultation"]},
            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            "time": {"$dateToString": {"format": "%H:%M", "date": "$date"}},
            "patient_name": "$patient_info.name",
            "patient_age": "$patient_info.age",
            "patient_gender": "$patient_info.gender",
            "medical_id": "$patient_info.medical_id"
        }}
    ])
    
    formatted_appointments = list(mongo.db.appointments.aggregate(pipeline))

    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "data": formatted_appointments
    })


# Doctor all patients
@doctor_bp.route("/doctors/patients", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_patients():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    skip = (page - 1) * per_page
    
    search = request.args.get("search")
    patient_filter = request.args.get("filter")

    match_query = {}
    
    if patient_filter and patient_filter != "All Patients":
        match_query["condition"] = patient_filter

    if search:
        match_query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"medical_id": {"$regex": search, "$options": "i"}},
                {"condition": {"$regex": search, "$options": "i"}}
            ]

    pipeline = []
    if match_query:
        pipeline.append({"$match": match_query})

    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.patients.aggregate(count_pipeline))
    total_items = count_result[0]["total"] if count_result else 0
    total_pages = (total_items + per_page - 1) // per_page if per_page else 0

    pipeline.extend([
        {"$skip": skip},
        {"$limit": per_page},
        {"$project": {
            "password": 0
        }},
        {"$project": {
            "_id": {"$toString": "$_id"},
            "medical_id": 1,
            "name": 1,
            "gender": 1,
            "age": 1,
            "condition": 1,
            "email": 1,
            "mobile": 1,
            "last_visit": {"$dateToString": {"format": "%Y-%m-%d", "date": "$last_visit"}},
            "admission_date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$admission_date"}}
        }}
    ])
    
    patients = list(mongo.db.patients.aggregate(pipeline))

    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "data": patients
    })


@doctor_bp.route("/doctors/patient-profile/<patient_id>", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def patient_profile(patient_id):
    data = request.json
    try:
        pid = ObjectId(patient_id)
    except:
        return jsonify({"error": "Invalid patient ID"}), 400

    patient = mongo.db.patients.find_one({"_id": pid}, {"password": 0})
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient)



    
# patient condition update
@doctor_bp.route("/patients/<patient_id>/condition", methods=["PUT"])
@jwt_required()
@role_required("Doctor")
def update_condition(patient_id):
    data = request.json
    try:
        pid = ObjectId(patient_id)
    except:
        return jsonify({"error": "Invalid patient ID"}), 400

    mongo.db.patients.update_one(
        {"_id": pid},
        {"$set": {"condition": data.get("condition", "")}}
    )

    return jsonify({"message": "Condition updated"})