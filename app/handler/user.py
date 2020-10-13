import time,uuid,os

import aiofiles
from tornado.escape import json_decode

from ..lib.route import route
from . import BaseHandler
from ..lib.decorator import authenticated
from ..lib.util import encode_auth_token
from ..models import User
from ..bootloader import settings

@route(r'/login', name='login')
class LoginHandler(BaseHandler):
    async def post(self):
        data = json_decode(self.request.body.decode())
        try:
            user = await self.application.objects.get(User, username=data['username'])
            if not user.check_pwd(data['password']):
                self.set_status(400)
                res = {'message': '密码错误', 'error': True}
            else:
                login_time = str(int(time.time()*1000))
                user.login_time = login_time
                update_user = await self.application.objects.update(user)
                if update_user:
                    token = encode_auth_token(user.id, login_time)
                    res = {'message': '登录成功', 'token': token, 'success': True}
                else:
                    self.set_status(400)
                    res = {'message': '登录失败', 'error': True}
        except User.DoesNotExist as e:
            self.set_status(400)
            res = {'message': '用户不存在', 'error': True}

        self.finish(res)


@route(r'/register', name='register')
class RegisterHandler(BaseHandler):
    async def post(self):
        data = json_decode(self.request.body.decode())
        try:
            exist_user = await self.application.objects.get(User, username=data['username'])
            self.set_status(400)
            res = {'message':'用户已存在', 'error': True}
        except User.DoesNotExist as e:
            user_data = {}
            user_data['username'] = data['username']
            user_data['password'] = data['password']
            login_time = str(int(time.time()*1000))
            user_data['login_time'] = login_time
            user = await self.application.objects.create(User, **user_data)
            if user:
                token = encode_auth_token(user.id, login_time)
                res = {'message': '注册成功', 'token': token, 'success': True}

        self.finish(res)


@route(r'/auth', name='auth')
class AuthHandler(BaseHandler):
    @authenticated
    async def get(self):
        self.finish({"test": 'auth'})


@route(r'/upload', name='upload')
class UploadHandler(BaseHandler):
    async def post(self):
        try:
            files = self.request.files['image']
            for file in files:
                name = str(uuid.uuid4()) + '.' +file['filename'].split('.')[-1]
                file_path = os.path.join(settings['UPLOAD_PATH'], name)
                body = file['body']
                async with aiofiles.open(file_path, 'wb') as fw:
                    await fw.write(body)
                rep = {'success': True, 'message': '上传成功'}
        except Exception as e:
            self.set_status(400)
            rep = {'error': True, 'message': '上传失败'}
        finally:
            self.finish(rep)
