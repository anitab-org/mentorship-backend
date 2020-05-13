from app.database.sqlalchemy_extension import db


class TokenModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.Integer, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, token_type, user_identity, expires , revoked):
   
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.expires = expires
        self.revoked = revoked

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()