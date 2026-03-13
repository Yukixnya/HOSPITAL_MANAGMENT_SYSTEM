from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from db import mongo

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():

    data = request.json
    role = data["role"]

    if role == "Admin":
        user = mongo.db.admins.find_one({"email": data["email"]})

    elif role == "Doctor":
        user = mongo.db.doctors.find_one({"email": data["email"]})

    elif role == "Patient":
        user = mongo.db.patients.find_one({"email": data["email"]})

    else:
        return jsonify({"error": "Invalid role"}), 400


    if not user:
        return jsonify({"error": "User not found"}), 404


    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401


    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": role}
    )

    return jsonify({"token": token})