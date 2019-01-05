from app.database.sqlalchemy_extension import DB


def reset_database():
    DB.drop_all()
    DB.create_all()
