
from app.database.models.token import TokenModel
from flask_jwt_extended import decode_token
from datetime import datetime



def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).

    """
    return datetime.fromtimestamp(epoch_utc)


class TokenDAO:

    def add_token_to_database(self, encoded_token, identity_claim):
        """
        Adds a new token to the database. It is not revoked when it is added.
        :param identity_claim:

        """
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        user_identity = decoded_token[identity_claim]
        expires = _epoch_utc_to_datetime(decoded_token['exp'])
        revoked = False

        token = TokenModel(jti, token_type, user_identity, expires, revoked)
        token.save_to_db()

    def revoke_tokens(self, user_id):
        """
        Revokes the given token. Raises a TokenNotFound error if the token does
        not exist in the database

        """
        tokens = TokenModel.query.filter_by(user_identity=user_id,revoked=False).all()
        for token in tokens:
            token.revoked = True
            token.commit_to_db()
        


