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




# -------------------------
# ID Generator of Appointment
# -------------------------
def get_next_appointment_id():
    counter = Counter.query.filter_by(id="appointment_id").first()
    if not counter:
        counter = Counter(id="appointment_id", seq=0)
        db.session.add(counter)
        db.session.commit()
        
    counter.seq += 1
    db.session.commit()
    
    return f"APT-{str(counter.seq).zfill(5)}"


# -------------------------
# Caching Utilities
# -------------------------
import json
from extensions import redis_client

def cache_get(key):
    """Get a cached value by exact key. Returns None on miss or Redis error."""
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None

def cache_set(key, value, ttl=300):
    """Serialize and store a value with an expiry (default 5 min)."""
    try:
        redis_client.set(key, json.dumps(value, default=str), ex=ttl)
    except Exception:
        pass  # Degrade gracefully — cache miss on next request is fine

def cache_delete(key):
    """Delete a single exact cache key."""
    try:
        redis_client.delete(key)
    except Exception:
        pass

def cache_delete_pattern(pattern):
    """Delete all keys matching a glob pattern (e.g. 'admin:appointments:*').
    Uses SCAN so it is safe on large key-spaces (non-blocking)."""
    try:
        keys = list(redis_client.scan_iter(match=pattern, count=100))
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass

def cache_flush():
    """Flush ALL keys from the current Redis DB. Admin-only operation."""
    try:
        redis_client.flushdb()
        return True
    except Exception:
        return False