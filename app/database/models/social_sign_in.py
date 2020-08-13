from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db

class SocialSignInModel(db.Model):
    """Data model representation of social sign in of a user.

    Attributes:
        user_id: user_id, to identify the user in user model
        social_sign_in_type: social sign in type (apple, google)
        id_token: id_token sent by the social sign in provider
        associated_email: email of the user associated with the social sign in provider
        full_name: full name of the user associated with the social sign in provider
    """

    # Specifying database table used for SocialSignInModel
    __tablename__ = "social_sign_in"
    __table_args__ = {"extend_existing": True}

    # data properties
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    social_sign_in_type = db.Column(db.String(20))
    id_token = db.Column(db.String(100), primary_key=True)
    associated_email = db.Column(db.String(50))
    full_name = db.Column(db.String(50))

    def __init__(self, user_id, sign_in_type, id_token, email, name):
        self.user_id = user_id
        self.social_sign_in_type = sign_in_type
        self.id_token = id_token
        self.associated_email = email
        self.full_name = name

    @classmethod
    def get_social_sign_in_details(cls, user_id: int, social_sign_in_type: str):
        """Returns social sign in details of the user for the specified type"""
        return cls.query.filter_by(user_id=user_id, social_sign_in_type=social_sign_in_type).first()

    @classmethod
    def find_by_id_token(cls, id_token: str):
        """Finds user using id_token"""
        return cls.query.filter_by(id_token=id_token).first()

    def save_to_db(self):
        """Adds the social sign in details to the database."""
        db.session.add(self)
        db.session.commit()