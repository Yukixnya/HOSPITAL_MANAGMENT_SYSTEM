from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify




# -------------------------
# Role Decorator
# -------------------------
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()

            if claims.get("role") != required_role:
                return jsonify({"error": "Unauthorized"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


from extensions import db
from models import Counter




# -------------------------
# ID Generator of Patient
# -------------------------
def get_next_medical_id():
    counter = Counter.query.filter_by(id="patient_id").first()
    if not counter:
        counter = Counter(id="patient_id", seq=0)
        db.session.add(counter)
        db.session.commit()
        
    counter.seq += 1
    db.session.commit()
    
    return f"MR-{str(counter.seq).zfill(5)}"




# -------------------------
# ID Generator of Doctor
# -------------------------
def get_next_doctor_id():
    counter = Counter.query.filter_by(id="doctor_id").first()
    if not counter:
        counter = Counter(id="doctor_id", seq=0)
        db.session.add(counter)
        db.session.commit()
        
    counter.seq += 1
    db.session.commit()
    
    return f"DOC-{str(counter.seq).zfill(5)}"