from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from auth.login import login_bp
from auth.register import register_bp
from flask_cors import CORS
from db import init_db

from routes.patients import patient_bp
from routes.doctors import doctor_bp
from routes.appointments import appointment_bp
from routes.admin import admin_bp


app = Flask(__name__)
app.config.from_object(Config)

init_db(app)

CORS(app, origins=["http://localhost:5173"])
jwt = JWTManager(app)

# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
app.register_blueprint(login_bp, url_prefix="/auth")
app.register_blueprint(register_bp, url_prefix="/auth")
app.register_blueprint(patient_bp, url_prefix="/api")
app.register_blueprint(doctor_bp, url_prefix="/api")
app.register_blueprint(appointment_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")

print(app.url_map)

@app.route("/")
def home():
    return {"message": "Hospital Backend Running 🚀"}

if __name__ == "__main__":
    app.run(debug=True , host="localhost" , port=5000)