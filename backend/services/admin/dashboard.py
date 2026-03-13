from db import mongo

def stat_data():

    total = mongo.db.doctors.count_documents({})
    active = mongo.db.doctors.count_documents({"status": "Active"})
    inactive = mongo.db.doctors.count_documents({"status": "Inactive"})
    on_leave = mongo.db.doctors.count_documents({"status": "On Leave"})
    patients = mongo.db.patients.count_documents({})
    appointments = mongo.db.appointments.count_documents({})

    return {
        "total_doctors": total,
        "total_active_doctors": active,
        "total_inactive_doctors": inactive,
        "total_onleave_doctors": on_leave,
        "total_patients": patients,
        "total_appointments": appointments
    }