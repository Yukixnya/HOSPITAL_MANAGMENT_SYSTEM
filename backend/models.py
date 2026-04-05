from extensions import db
from datetime import datetime

class Counter(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    seq = db.Column(db.Integer, default=0)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=True)
    specialization = db.Column(db.String(100))
    experience = db.Column(db.Integer, default=0)
    schedule = db.Column(db.String(255))
    status = db.Column(db.String(50), default="Active")
    clinic = db.Column(db.String(255), default="")
    rating = db.Column(db.Float, default=0.0)
    reviews = db.Column(db.Integer, default=0)
    fee = db.Column(db.Float, default=0.0)
    online = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, default="")
    education = db.Column(db.String(255), default="")
    languages = db.Column(db.String(255), default="English")
    specializations = db.Column(db.String(255), default="")

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=True)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    condition = db.Column(db.String(255), default="Observing")
    last_visit = db.Column(db.DateTime, nullable=True)
    dob = db.Column(db.String(50), default="")
    address = db.Column(db.String(255), default="")
    blood_type = db.Column(db.String(20), default="")
    preferences = db.Column(db.Text, default="[]")

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.DateTime)
    type = db.Column(db.String(100), default="Consultation")
    status = db.Column(db.String(50), default="Pending")
    diagnosisTitle = db.Column(db.String(255), default="Pending Assessment")
    diagnosisDesc = db.Column(db.Text, default="Awaiting official notes.")
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)
    date = db.Column(db.String(50))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    name = db.Column(db.String(255))
    dosage = db.Column(db.String(255))
    frequency = db.Column(db.String(255))
    duration = db.Column(db.String(255))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    text = db.Column(db.Text)
    date = db.Column(db.String(50))

class Vital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)
    label = db.Column(db.String(100))
    value = db.Column(db.String(50))
    unit = db.Column(db.String(50))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    author = db.Column(db.String(255))
    rating = db.Column(db.Float)
    date = db.Column(db.String(50))
    comment = db.Column(db.Text)


