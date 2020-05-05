from app.database.sqlalchemy_extension import db


def reset_database() -> None:
    db.drop_all()
    db.create_all()
