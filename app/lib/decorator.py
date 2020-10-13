import functools

from .util import decode_auth_token
from ..models import User

# 检查登录装饰器
def authenticated(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        message = ''
        auth = self.request.headers.get('Authorization', None)
        auth_list = auth.split(' ') if auth else None
        if auth_list and len(auth_list) == 2 and auth_list[0] == 'Basic':
            payload = decode_auth_token(auth_list[1])
            if isinstance(payload, str):
                message = 'Token错误'
                self.set_status(401)
            else:
                user_id = payload['data']['id']
                login_time = payload['data']['login_time']
                try:
                    user = await self.application.objects.get(User, id=user_id)
                    if user.login_time == login_time:
                        await method(self, *args, **kwargs)
                    else:
                        self.set_status(401)
                        message = '用户已登录'
                except User.DoesNoteExist as e:
                    self.set_status(401)
                    message = '用户未找到'
        else:
            self.set_status(401)
            message = '鉴权参数错误'

        self.finish({
            'error': True,
            'message': message
        })

    return wrapper