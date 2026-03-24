# HOSPITAL MANAGEMENT SYSTEM

## TECH STACK
* FLASK (API framework)
* VUE JS (Frontend)
* SQLITE (Database - Migrated from MongoDB)

---

## API Documentation

Below is a comprehensive list of all backend APIs available in the system. Every request under `/api/` (and `/auth/logout`) requires an `Authorization: Bearer <token>` header unless explicitly stated otherwise.

### 1. AUTHENTICATION APIs

#### Login User
- **Method & URL**: `POST /auth/login`
- **Input Sample**:
  ```json
  {
    "email": "smith@hms.com",
    "password": "doc123",
    "role": "Doctor"
  }
  ```
- **Response Sample**: `{"token": "eyJhbG...", "user": {"id": 1, "name": "Dr. Smith", ...}}`

#### Logout User
- **Method & URL**: `POST /auth/logout`
- **Response Sample**: `{"message": "Logged out successfully"}`

#### Register User
- **Method & URL**: `POST /auth/register`
- **Input Sample (Patient)**:
  ```json
  {
    "role": "Patient",
    "name": "Jane Doe",
    "age": 25,
    "gender": "Female",
    "mobile": "1231231234",
    "email": "jane@email.com",
    "password": "password123"
  }
  ```
- *(Admin requires only: name, email, password, role).*
- **Response Sample**: `{"message": "User registered successfully"}`

---

### 2. GENERAL / SHARED APIs

#### Upload Profile Image
- **Method & URL**: `POST /api/upload-profile-image`
- **Input Sample**: `multipart/form-data` with `image` file
- **Response Sample**: `{"message": "File uploaded successfully", "image_url": "http://localhost:5000/static/uploads/uuid.png"}`

#### Book Single Appointment
- **Method & URL**: `POST /api/appointments`
- **Input Sample**:
  ```json
  {
    "doctor_id": "1",
    "date": "2026-03-25T10:30",
    "type": "Consultation",
    "location": "Main Hospital"
  }
  ```
- **Response Sample**: `{"message": "Appointment created successfully"}`

#### Bulk Book Appointments
- **Method & URL**: `POST /api/appointments/bulk`
- **Input Sample**:
  ```json
  [
    {"doctor_id": "1", "date": "2026-04-01T14:00", ...},
    {"doctor_id": "2", "date": "2026-04-02T15:00", ...}
  ]
  ```

---

### 3. ADMIN APIs (Requires Admin Token)

#### Global Stats
- **Method & URL**: `GET /api/admin`
- **Response Sample**:
  ```json
  {
    "total_doctors": 10,
    "total_active_doctors": 8,
    "total_patients": 55,
    "total_appointments": 120
  }
  ```

#### Get All Patients
- **Method & URL**: `GET /api/admin/patients`
- **Response Sample**: `[{"_id": "1", "medical_id": "MR-0001", "name": "Jane Doe", ...}]`

#### Get All Appointments
- **Method & URL**: `GET /api/admin/appointments`
- **Response Sample**: `[{"_id": "1", "patient_id": "2", "doctor_id": "1", "status": "Confirmed", ...}]`

#### Appointment Trend
- **Method & URL**: `GET /api/admin/appointments-trend`
- **Response Sample**: `{"labels": ["Mon", "Tue"], "data": [5, 12]}`

#### Get All Doctors Detailed
- **Method & URL**: `GET /api/admin/doctors`
- **Response Sample**: `[{"_id": "1", "doctor_id": "DOC-0001", "name": "Dr. Smith", "status": "Active", ...}]`

#### Get Doctors Names Only
- **Method & URL**: `GET /api/admin/doctors_name`
- **Response Sample**: `[{"id": 1, "name": "Dr. Smith"}]`

#### Add Single Doctor
- **Method & URL**: `POST /api/admin/add-doctor`
- **Input Sample**: 
  ```json
  {
    "name": "Dr. House",
    "email": "house@hms.com",
    "password": "password",
    "gender": "Male",
    "mobile": "9998887777",
    "specialization": "Diagnostics"
  }
  ```

#### Bulk Add Doctors
- **Method & URL**: `POST /api/admin/bulk-add-doctor`
- **Input Sample**: Array of Doctor objects (same as Single Doctor).

#### Update Doctor Status
- **Method & URL**: `PUT /api/admin/doctors/<doctor_id>/status`
- **Input Sample**: `{"status": "Inactive"}`

#### Update Doctor Profile
- **Method & URL**: `PUT /api/admin/doctors/<doctor_id>`
- **Input Sample**: `{"mobile": "555-5555", "experience": 15}`

#### Delete Doctor
- **Method & URL**: `DELETE /api/admin/doctors/<doctor_id>`
- **Response Sample**: `{"message": "Doctor deactivated"}`

---

### 4. DOCTOR APIs (Requires Doctor Token)

#### My Profile Complete
- **Method & URL**: `GET /api/doctors/me`
- **Response Sample**: `{"_id": "1", "name": "Dr. Smith", "specialization": "Cardiology", "reviews": 15}`

#### Doctor Dashboard
- **Method & URL**: `GET /api/doctor/dashboard`
- **Response Sample**: `{"todaysAppointments": 5, "totalPatients": 120, "rating": 4.8}`

#### My Assigned Appointments
- **Method & URL**: `GET /api/doctors/my-appointments`
- **Response Sample**: `[{"_id": "10", "patientName": "Jane Doe", "date": "2026-03-24T09:00", ...}]`

#### My Patients Roster
- **Method & URL**: `GET /api/doctors/patients`
- **Response Sample**: `[{"id": "5", "name": "Jane Doe", "condition": "Recovering", ...}]`

#### Single Patient Profile
- **Method & URL**: `GET /api/doctors/patient-profile/<patient_id>`
- **Response Sample**: `{"profile": {"name": "Jane Doe", "age": 25}, "history": [...]}`

#### Update Patient Condition
- **Method & URL**: `PUT /api/patients/<patient_id>/condition`
- **Input Sample**: `{"condition": "Stable / Recovering"}`
- **Response Sample**: `{"message": "Patient condition updated"}`

#### Add Prescription to Appointment
- **Method & URL**: `POST /api/doctors/appointments/<apt_id>/prescription`
- **Input Sample**:
  ```json
  {
    "name": "Amoxicillin",
    "dosage": "500mg",
    "frequency": "Twice a day",
    "duration": "7 days"
  }
  ```

#### Add Note to Appointment
- **Method & URL**: `POST /api/doctors/appointments/<apt_id>/note`
- **Input Sample**: `{"text": "Patient is experiencing mild headaches. Recommended rest."}`

#### Add Vital to Appointment
- **Method & URL**: `POST /api/doctors/appointments/<apt_id>/vital`
- **Input Sample**: `{"label": "Blood Pressure", "value": "120/80", "unit": "mmHg"}`

---

### 5. PATIENT APIs (Requires Patient Token)

#### My Profile Details
- **Method & URL**: `GET /api/patients/me`
- **Response Sample**: `{"profile": {"name": "Jane Doe", "mobile": "1231231234"}, "preferences": [...]}`

#### Update Profile Details
- **Method & URL**: `PUT /api/patients/update`
- **Input Sample**: `{"mobile": "0987654321", "address": "123 New Ave"}`

#### Patient Dashboard
- **Method & URL**: `GET /api/patients/dashboard`
- **Response Sample**: `{"nextAppointment": {...}, "vitals": [{"label": "Heart Rate", "value": "80 bpm", "icon": "❤️"}]}`

#### Browse Active Doctors
- **Method & URL**: `GET /api/patients/doctors?page=1&search=Cardio`
- **Response Sample**: `{"data": [{"name": "Dr. Smith", "specialty": "Cardiology"}], "pagination": {...}}`

#### Doctor Profile Details
- **Method & URL**: `GET /api/patients/doctors/<doc_id>`
- **Response Sample**: `{"doctor": {"name": "Dr. Smith", "fee": 150}, "reviews": [...]}`

#### My Internal Appointments
- **Method & URL**: `GET /api/patients/my-appointments`
- **Response Sample**: `{"upcoming": [...], "pastVisits": [...]}`

#### Specific Appointment Details
- **Method & URL**: `GET /api/patients/appointments/<apt_id>`
- **Response Sample**: `{"appointment": {...}, "prescriptions": [...], "notes": [...], "vitals": [...]}`

#### Full Medical History
- **Method & URL**: `GET /api/patients/medical-history`
- **Response Sample**: `{"vitals": [...], "medicalRecords": [...]}`

#### Leave Doctor Review
- **Method & URL**: `POST /api/patients/doctors/<doc_id>/review`
- **Input Sample**: `{"rating": 4.5, "comment": "Great doctor, very helpful!"}`

#### Export CSV Medical History
- **Method & URL**: `POST /api/patients/export-csv`
- **Response Sample**: `{"message": "CSV export facility is temporarily disabled..."}`
