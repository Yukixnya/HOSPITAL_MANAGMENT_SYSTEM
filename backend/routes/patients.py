from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from bson import ObjectId
from db import mongo
from datetime import datetime

patient_bp = Blueprint("patients", __name__)

# -----------------------------
# 1. Patient Profile
# -----------------------------
@patient_bp.route("/patients/me", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_my_profile():
    user_id = get_jwt_identity()
    patient = mongo.db.patients.find_one({"_id": ObjectId(user_id)}, {"password": 0})

    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404

    profile = {
        "_id": str(patient["_id"]),
        "fullName": patient.get("name", "Unknown"),
        "email": patient.get("email", ""),
        "phone": patient.get("mobile", ""),
        "dob": patient.get("dob", ""),
        "address": patient.get("address", "")
    }
    
    preferences = patient.get("preferences", [])

    return jsonify({"profile": profile, "preferences": preferences})


@patient_bp.route("/patients/update", methods=["PUT"])
@jwt_required()
@role_required("Patient")
def update_patient():
    user_id = get_jwt_identity()
    data = request.json

    update_fields = {}
    if "fullName" in data: update_fields["name"] = data["fullName"]
    if "phone" in data: update_fields["mobile"] = data["phone"]
    if "dob" in data: update_fields["dob"] = data["dob"]
    if "address" in data: update_fields["address"] = data["address"]
    if not update_fields:
        update_fields = data

    mongo.db.patients.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )

    return jsonify({"message": "Profile updated"})

# -----------------------------
# 2. Patient Dashboard
# -----------------------------
@patient_bp.route("/patients/dashboard", methods=["GET"])
@jwt_required()
@role_required("Patient")
def patient_dashboard():
    user_id = get_jwt_identity()
    query_id = ObjectId(user_id) if isinstance(user_id, str) and len(user_id)==24 else user_id
    
    # Get Next Appointment
    now = datetime.utcnow()
    pipeline = [
        {"$match": {"patient_id": query_id, "date": {"$gte": now}}},
        {"$sort": {"date": 1}},
        {"$limit": 1},
        {"$lookup": {"from": "doctors", "localField": "doctor_id", "foreignField": "_id", "as": "doctor_info"}},
        {"$unwind": {"path": "$doctor_info", "preserveNullAndEmptyArrays": True}}
    ]
    
    next_apt_cursor = list(mongo.db.appointments.aggregate(pipeline))
    next_appointment = None
    
    if next_apt_cursor:
        doc = next_apt_cursor[0]
        dt = doc.get("date")
        diff = dt - now if dt else None
        
        days, hours, mins = 0, 0, 0
        if diff:
            days = diff.days
            secs = diff.seconds
            hours = secs // 3600
            mins = (secs % 3600) // 60
            
        next_appointment = {
            "id": str(doc["_id"]),
            "days": str(days).zfill(2),
            "hours": str(hours).zfill(2),
            "mins": str(mins).zfill(2),
            "doctorName": doc.get("doctor_info", {}).get("name", "Unknown Dr."),
            "doctorImage": f"https://ui-avatars.com/api/?name={doc.get('doctor_info', {}).get('name', 'Doc')}",
            "type": doc.get("type", "Consultation"),
            "dateFormatted": dt.strftime("%A, %b %d • %I:%M %p") if dt else "",
            "status": doc.get("status", "Confirmed")
        }

    # Fetch DB Vitals
    vitals_db = list(mongo.db.vitals.find({"patient_id": query_id}).limit(3))
    vitals = []
    for v in vitals_db:
        # Dynamic UI mapping wrapper
        color = "bg-blue-600" if "Heart" in v.get("label", "") else "bg-orange-500"
        icon = "❤️" if "Heart" in v.get("label", "") else "💧"
        vitals.append({
            "label": v.get("label"), 
            "value": f"{v.get('value')} {v.get('unit', '')}", 
            "pct": 70, 
            "color": color, 
            "icon": icon
        })
    
    # # Dynamically pull doctor specialities for the dashboard categories
    # unique_specs = mongo.db.doctors.distinct("specialization")
    # specializations = []
    # colors = [('text-red-400', 'bg-red-50', '❤️'), ('text-blue-400', 'bg-blue-50', '🧠'), 
    #           ('text-green-400', 'bg-green-50', '🍏'), ('text-purple-400', 'bg-purple-50', '🌿')]
    
    # for i, spec in enumerate(unique_specs):
    #     if spec:
    #         c = colors[i % len(colors)]
    #         specializations.append({"name": spec, "icon": c[2], "bg": f"{c[1]} {c[0]}"})

    return jsonify({"nextAppointment": next_appointment, "vitals": vitals})

# -----------------------------
# 3. Doctors List
# -----------------------------
@patient_bp.route("/patients/doctors", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_doctors_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    skip = (page - 1) * per_page
    search = request.args.get('search')

    query = {"status": "Active"}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"specialization": {"$regex": search, "$options": "i"}}
        ]
    
    total_items = mongo.db.doctors.count_documents(query)
    total_pages = (total_items + per_page - 1) // per_page if per_page else 0

    doctors_cursor = mongo.db.doctors.find(query).skip(skip).limit(per_page)
    
    result = []
    for d in doctors_cursor:
        result.append({
            "id": str(d["_id"]),
            "name": d.get("name"),
            "specialty": d.get("specialization", "General"),
            "clinic": d.get("clinic", ""),
            "rating": d.get("rating", 0.0),
            "reviews": d.get("reviews", 0),
            "fee": d.get("fee", 0),
            "online": d.get("online", False),
            "bio": d.get("bio", ""),
            "image": f"https://ui-avatars.com/api/?name={d.get('name', 'Doc')}"
        })
        
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "data": result
    })

# -----------------------------
# 4. Doctor Profile
# -----------------------------
@patient_bp.route("/patients/doctors/<doc_id>", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_doctor_profile(doc_id):
    try:
        did = ObjectId(doc_id)
    except:
        return jsonify({"error": "Invalid doctor ID"}), 400
        
    d = mongo.db.doctors.find_one({"_id": did})
    if not d:
        return jsonify({"error": "Doctor not found"}), 404
        
    doctor = {
        "id": str(d["_id"]),
        "name": d.get("name"),
        "image": f"https://ui-avatars.com/api/?name={d.get('name', 'D')}",
        "title": d.get("specialization", "Doctor"),
        "education": d.get("education", ""),
        "experience": f"{d.get('experience', 0)}+ Years",
        "languages": d.get("languages", ["English"]),
        "rating": d.get("rating", 0.0),
        "patientCount": "Verified",
        "reviews": f'{d.get("reviews", 0)}+',
        "fee": d.get("fee", 0),
        "specializations": d.get("specializations", [d.get("specialization", "General Care")]),
        "bio_p1": d.get("bio", ""),
        "bio_p2": ""
    }
    
    db_reviews = list(mongo.db.reviews.find({"doctor_id": did}).limit(5))
    reviews = []
    for idx, r in enumerate(db_reviews):
        reviews.append({
            "id": str(r["_id"]), "author": r.get("author", "Patient"), 
            "rating": r.get("rating", 5), "date": r.get("date", "Recently"),
            "comment": r.get("comment", "")
        })
    
    return jsonify({"doctor": doctor, "reviews": reviews})

# -----------------------------
# 5. My Appointments
# -----------------------------
@patient_bp.route("/patients/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_my_appointments():
    user_id = get_jwt_identity()
    query_id = ObjectId(user_id) if isinstance(user_id, str) and len(user_id)==24 else user_id
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    skip = (page - 1) * per_page
    search = request.args.get('search')

    pipeline = [
        {"$match": {"patient_id": query_id}},
        {"$lookup": {"from": "doctors", "localField": "doctor_id", "foreignField": "_id", "as": "doctor_info"}},
        {"$unwind": {"path": "$doctor_info", "preserveNullAndEmptyArrays": True}}
    ]

    if search:
        pipeline.append({
            "$match": {
                "$or": [
                    {"doctor_info.name": {"$regex": search, "$options": "i"}},
                    {"doctor_info.specialization": {"$regex": search, "$options": "i"}},
                    {"type": {"$regex": search, "$options": "i"}},
                    {"status": {"$regex": search, "$options": "i"}}
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
        {"$limit": per_page}
    ])

    appointments = list(mongo.db.appointments.aggregate(pipeline))
    
    now = datetime.utcnow()
    upcoming = []
    past = []
    
    for apt in appointments:
        dt = apt.get("date")
        if not dt: continue
        
        status = apt.get("status", "Confirmed")
        doc_name = apt.get("doctor_info", {}).get("name", "Unknown Dr.")
        spec = apt.get("doctor_info", {}).get("specialization", "General")
        
        is_past = dt < now
        
        if is_past:
            past.append({
                "id": str(apt["_id"]),
                "date": dt.strftime("%b %d, %Y"),
                "doctor": doc_name,
                "department": spec,
                "type": apt.get("type", "Consultation"),
                "img": f"https://ui-avatars.com/api/?name={doc_name}"
            })
        else:
            status_class = "bg-orange-100 text-orange-600" if status.lower() == "pending" else "bg-green-100 text-green-600"
            upcoming.append({
                "id": str(apt["_id"]),
                "month": dt.strftime("%b").upper(),
                "day": dt.strftime("%d"),
                "doctor": doc_name,
                "specialty": spec,
                "type": apt.get("type", "Consultation"),
                "time": dt.strftime("%I:%M %p"),
                "location": apt.get("location", "Main Hospital"),
                "status": status.capitalize(),
                "statusClass": status_class
            })
            
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "upcomingAppointments": upcoming, 
        "pastVisits": past
    })

# -----------------------------
# 6. Past Appointment Details
# -----------------------------
@patient_bp.route("/patients/appointments/<apt_id>", methods=["GET"])
@jwt_required()
@role_required("Patient")
def appointment_details(apt_id):
    try:
        aid = ObjectId(apt_id)
    except:
        return jsonify({"error": "Invalid appointment ID"}), 400
        
    pipeline = [
        {"$match": {"_id": aid}},
        {"$lookup": {"from": "doctors", "localField": "doctor_id", "foreignField": "_id", "as": "doctor_info"}},
        {"$unwind": {"path": "$doctor_info", "preserveNullAndEmptyArrays": True}}
    ]
    
    results = list(mongo.db.appointments.aggregate(pipeline))
    if not results: return jsonify({"error": "Appointment not found"}), 404
        
    doc = results[0]
    dt = doc.get("date")
    doc_info = doc.get("doctor_info", {})
    
    details = {
        "dateFormatted": dt.strftime("%B %d, %Y") if dt else "Unknown Date",
        "doctorName": doc_info.get("name", "Unknown Dr."),
        "doctorDepartment": doc_info.get("specialization", "General"),
        "doctorImage": f"https://ui-avatars.com/api/?name={doc_info.get('name', 'D')}",
        "diagnosisTitle": doc.get("diagnosisTitle", "Pending Assessment"),
        "diagnosisCode": doc.get("diagnosisCode", "-"),
        "diagnosisStatus": doc.get("status", "Pending"),
        "diagnosisDesc": doc.get("diagnosisDesc", "Awaiting official notes."),
    }
    
    # Direct DB Fetching
    prescriptions = list(mongo.db.prescriptions.find({"appointment_id": aid}, {"_id": 0}))
    notes = list(mongo.db.notes.find({"appointment_id": aid}, {"_id": 0}))
    visitVitals = list(mongo.db.vitals.find({"appointment_id": aid}, {"_id": 0}))
    
    return jsonify({
        "details": details,
        "prescriptions": prescriptions,
        "notes": notes,
        "visitVitals": visitVitals
    })
    
# -----------------------------
# 7. Medical History
# -----------------------------
@patient_bp.route("/patients/medical-history", methods=["GET"])
@jwt_required()
@role_required("Patient")
def medical_history():
    user_id = get_jwt_identity()
    query_id = ObjectId(user_id) if isinstance(user_id, str) and len(user_id)==24 else user_id

    page = request.args.get('page', 1, type=int)
    per_page = 10
    skip = (page - 1) * per_page
    search = request.args.get('search')
    
    base_query = {"patient_id": query_id}
    if search:
        base_query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"provider": {"$regex": search, "$options": "i"}}
        ]
    
    total_items = mongo.db.medical_records.count_documents(base_query)
    total_pages = (total_items + per_page - 1) // per_page if per_page else 0

    records_db = list(mongo.db.medical_records.find(base_query).skip(skip).limit(per_page))
    medicalRecords = []
    
    for r in records_db:
        medicalRecords.append({
            "id": str(r["_id"]),
            "type": r.get("type", "Report"),
            "date": r.get("date", "Unknown Date"),
            "time": r.get("time", "10:00 AM"),
            "title": r.get("title", ""),
            "description": r.get("description", ""),
            "provider": r.get("provider", ""),
            "status": r.get("status", "Ready"),
            "icon": r.get("icon", "🏥"),
            "markerClass": r.get("markerClass", "text-blue-600 ring-4 ring-blue-50"),
            "tagClass": r.get("tagClass", "bg-blue-50 text-blue-600"),
            "actionLabel": r.get("actionLabel", "View")
        })

    # Stats use global unfiltered quantities bounds
    global_total = mongo.db.medical_records.count_documents({"patient_id": query_id})
    lab_tests_count = mongo.db.medical_records.count_documents({"patient_id": query_id, "type": "Lab Report"})
    encounters_count = mongo.db.medical_records.count_documents({"patient_id": query_id, "type": "Clinical Visit"})

    historyStats = [
      {"label": 'Diagnoses', "value": str(global_total), "icon": '💼', "bgClass": 'bg-blue-50 text-blue-600'},
      {"label": 'Lab Tests', "value": str(lab_tests_count), "icon": '🔬', "bgClass": 'bg-green-50 text-green-600'},
      {"label": 'Encounters', "value": str(encounters_count), "icon": '🏥', "bgClass": 'bg-purple-50 text-purple-600'},
      {"label": 'Archived', "value": '0', "icon": '📑', "bgClass": 'bg-orange-50 text-orange-600'}
    ]
    
    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "historyStats": historyStats,
        "medicalRecords": medicalRecords
    })