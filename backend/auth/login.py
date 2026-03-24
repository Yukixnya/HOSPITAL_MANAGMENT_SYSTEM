from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import Admin, Doctor, Patient

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():

    data = request.json
    role = data.get("role")

    if role == "Admin":
        user = Admin.query.filter_by(email=data["email"]).first()
    elif role == "Doctor":
        user = Doctor.query.filter_by(email=data["email"]).first()
    elif role == "Patient":
        user = Patient.query.filter_by(email=data["email"]).first()
    else:
        return jsonify({"error": "Invalid role"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": role}
    )

    return jsonify({"token": token})

@login_bp.route('/logout', methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"})
