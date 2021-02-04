import jwt
import datetime
import Utils.configs as configs

# https://realpython.com/token-based-authentication-with-flask/#jwt-setup

# Encode authorization token
def encode_auth_token(user_email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_email
        }
        return jwt.encode(payload, configs.JWT_SECRET_KEY, configs.JWT_ALGORITHM)
    except Exception: 
        return 'Error: Problem generating token.'

# Decode authorization token
def decode_auth_token(token):
    try:
        payload = jwt.decode(token, configs.JWT_SECRET_KEY, configs.JWT_ALGORITHM)
        return True, payload['sub']
    except jwt.ExpiredSignatureError: 
        return False, 'Error: Signature expired. Please log in again.'
    except jwt.InvalidTokenError: 
        return False, 'Error: Invalid token. Please log in again.'

