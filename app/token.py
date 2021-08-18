from app import app
from itsdangerous import URLSafeTimedSerializer

#generates token to be attached to end of confirmation link
#token is encrypted, contains user email and expiration
#token is appended to url and sent to user, on click, confirms user's email
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="confirmation_token")

#confirms that a given token has not expired and has not been tampered with
#each token is valid for 3600 seconds (1 hour)
#if valid, returns email, if invalid, returns false
def check_token(token, valid_for=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="confirmation_token", max_age=valid_for)
    except:
        return False
    return email
