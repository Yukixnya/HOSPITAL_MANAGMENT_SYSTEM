from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import Admin, Patient
from extensions import db
from utils import get_next_medical_id
from datetime import datetime

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():

    data = request.json
    role = str(data.get("role", "")).capitalize()

    if role == "Admin":
        if Admin.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Admin already exists"}), 400

        admin = Admin(
            name=data["name"],
            email=data["email"],
            password=generate_password_hash(str(data["password"]))
        )
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "Admin created"}), 201

    elif role == "Patient":
        if Patient.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 400

        medical_id = get_next_medical_id()
        patient = Patient(
            medical_id=medical_id,
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            mobile=data["mobile"],
            admission_date=datetime.utcnow(),
            condition="Observing",
            email=data["email"],
            password=generate_password_hash(str(data["password"]))
        )
        db.session.add(patient)
        db.session.commit()

        return jsonify({
            "message": "Patient registered",
            "medical_id": medical_id
        }), 201

    else:
        return jsonify({"error": "Invalid role"}), 400
