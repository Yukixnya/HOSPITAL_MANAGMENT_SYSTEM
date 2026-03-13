from db import mongo
from werkzeug.security import generate_password_hash

def add_one_doctor(data):

    if mongo.db.doctors.find_one({"email": data["email"]}):
        return {"error": "Email already exists"}, 400

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

    return {"message": "Doctor created successfully"}, 201


def add_many_doctor(data):

    users = []

    for i in data:
            if mongo.db.doctors.find_one({"email": i["email"]}):
                return {"error": "Email already exists"}, 400

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

    return {
        "message": "Doctors registered",
        "count": len(users)
    }, 201