import jwt
import datetime
import Utils.constants as constants

# https://realpython.com/token-based-authentication-with-flask/#jwt-setup

# Encode authorization token
def encode_auth_token(user_email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_email
        }
        return jwt.encode(
            payload,
            constants.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception: return 'Error'

# Decode authorization token
@staticmethod
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, constants.SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'