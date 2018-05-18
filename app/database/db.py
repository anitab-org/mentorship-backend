from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def reset_database():
    from app.database.models.user import UserModel
    db.drop_all()
    db.create_all()
