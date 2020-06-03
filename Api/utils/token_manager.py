import datetime
from flask_jwt_extended import ( 
    create_access_token, 
    create_refresh_token,
)

TOKEN_EXPIRE_MINUTE = 60

def access_token_expire_time():
    return datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTE)

def generate_tokens(user):
    expires = access_token_expire_time()
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    refresh_token = create_refresh_token(identity=str(user.id))
    expires_time = datetime.datetime.now() + datetime.timedelta(minutes = TOKEN_EXPIRE_MINUTE)
    return {'access_token': access_token, 
                    'refresh_token': refresh_token,
                    'expires_at': int(expires_time.strftime("%s"))}

def refresh_a_token(current_user):
    expires = datetime.timedelta(minutes=60)
    expires_time = datetime.datetime.now() + datetime.timedelta(minutes = TOKEN_EXPIRE_MINUTE)
    return {
            'access_token': create_access_token(identity=current_user, 
            expires_delta=expires),
            'expires_at': int(expires_time.strftime("%s"))
    }
