from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from db import mongo
from utils import get_next_medical_id
from datetime import datetime

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():

    data = request.json
    role = data["role"]

    if role == "Admin":

        if mongo.db.admins.find_one({"email": data["email"]}):
            return jsonify({"error": "Admin already exists"}), 400

        admin = {
            "name": data["name"],
            "email": data["email"],
            "password": generate_password_hash(str(data["password"]))
        }

        mongo.db.admins.insert_one(admin)

        return jsonify({"message": "Admin created"}), 201


    elif role == "Patient":

        if mongo.db.patients.find_one({"email": data["email"]}):
            return jsonify({"error": "Email already exists"}), 400

        medical_id = get_next_medical_id()

        patient = {
            "medical_id": medical_id,
            "name": data["name"],
            "age": data["age"],
            "gender": data["gender"],
            "mobile": data["mobile"],
            "admission_date": datetime.utcnow(),
            "condition": "Observing",
            "last_visit": None,
            "email": data["email"],
            "password": generate_password_hash(str(data["password"]))
        }

        mongo.db.patients.insert_one(patient)

        return jsonify({
            "message": "Patient registered",
            "medical_id": medical_id
        }), 201


    else:
        return jsonify({"error": "Invalid role"}), 400