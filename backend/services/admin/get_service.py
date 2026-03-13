from datetime import datetime
from db import mongo
import math

def all_doctors(page=1, search=None):

    per_page = 10
    skip = (page - 1) * per_page

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

    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})

    count_result = list(mongo.db.doctors.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page) if total else 0

    pipeline.extend([
        {"$sort": {"experience": -1}},
        {"$skip": skip},
        {"$limit": per_page},
        {"$project": {"password": 0}}
    ])

    doctors = list(mongo.db.doctors.aggregate(pipeline))

    for d in doctors:
        d["_id"] = str(d["_id"])

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": doctors
    }, 200

def all_patients(page=1, search=None):

    per_page = 10
    skip = (page - 1) * per_page

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

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": patients
    }, 200

def all_appointments(page=1, search=None):

    per_page = 10
    skip = (page - 1) * per_page

    pipeline = [
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {"$unwind": "$patient"},
        {
            "$lookup": {
                "from": "doctors",
                "localField": "doctor_id",
                "foreignField": "_id",
                "as": "doctor"
            }
        },
        {"$unwind": "$doctor"}
    ]

    if search:
        pipeline.append({
            "$match": {
                "$or": [
                    {"patient.name": {"$regex": search, "$options": "i"}},
                    {"patient.medical_id": {"$regex": search, "$options": "i"}},
                    {"doctor.name": {"$regex": search, "$options": "i"}}
                ]
            }
        })

    # Count total
    count_pipeline = pipeline.copy()
    count_pipeline.append({"$count": "total"})
    count_result = list(mongo.db.appointments.aggregate(count_pipeline))

    total = count_result[0]["total"] if count_result else 0
    total_pages = math.ceil(total / per_page) if total else 0

    # Final output format
    pipeline.append({
        "$project": {
            "_id": 1,
            "patient_id": "$patient.medical_id",
            "patient_name": "$patient.name",
            "doctor_name": "$doctor.name",
            "department": "$doctor.specialization",
            "status": 1,
            "time": {
                "$dateToString": {
                    "format": "%H:%M",
                    "date": "$date"
                }
            },
            "date": {
                "$dateToString": {
                    "format": "%b %d, %Y",
                    "date": "$date"
                }
            }
        }
    })

    # Pagination
    pipeline.append({"$sort": {"date": -1}})
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": per_page})

    appointments = list(mongo.db.appointments.aggregate(pipeline))

    for a in appointments:
        a["_id"] = str(a["_id"])
        dt = datetime.strptime(a["time"], "%H:%M")
        a["time"] = dt.strftime("%I:%M %p")

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": appointments
    }, 200