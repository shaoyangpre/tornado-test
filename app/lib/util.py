import jwt, datetime

from app.bootloader import settings


def encode_auth_token(user_id, login_time):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings['TOKEN_EXP']),
        'iat': datetime.datetime.utcnow(),
        'iss': 'shaoyang',
        'data': {
            'id': user_id,
            'login_time': login_time
        }
    }
    return str(jwt.encode(
        payload,
        settings['SECRET_KEY'],
        algorithm='HS256'
    ), 'utf-8')


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, settings['SECRET_KEY'])
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'


if __name__ == '__main__':
    print(encode_auth_token(1, '2020'))
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDI1MDgzNDYsImlhdCI6MTYwMjUwODM0MiwiaXNzIjoic2hhb3lhbmciLCJkYXRhIjp7ImlkIjoxLCJsb2dpbl90aW1lIjoiMjAyMCJ9fQ.RvpA8O07q0TjFGFikfuM4zF5qKmjVGEhj-z7pCGAinU'
    # data = decode_auth_token(token)
    pass
