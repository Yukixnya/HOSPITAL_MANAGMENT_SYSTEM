import os
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from models import Admin, Doctor, Patient
from extensions import db

upload_bp = Blueprint("uploads", __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload-profile-image", methods=["POST"])
@jwt_required()
def upload_profile_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image field in request"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")
        
        # Base URL
        image_url = f"http://localhost:5000/static/uploads/{unique_filename}"
        
        user = None
        if role == "Admin":
            user = Admin.query.get(user_id)
        elif role == "Doctor":
            user = Doctor.query.get(user_id)
        elif role == "Patient":
            user = Patient.query.get(user_id)
            
        if user:
            user.image_url = image_url
            db.session.commit()
            return jsonify({"message": "File uploaded successfully", "image_url": image_url}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    return jsonify({"error": "Invalid file type"}), 400
