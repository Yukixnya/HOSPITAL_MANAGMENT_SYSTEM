import os
from dotenv import load_dotenv
from extensions import db

load_dotenv()

def init_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    with app.app_context():
        import models
        db.create_all()