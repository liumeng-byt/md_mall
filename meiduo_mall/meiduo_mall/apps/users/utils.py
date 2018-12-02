# 因为要返回多个参数token,user_id,username,所以需要重新定义一个函数,创建后需要把源代码里的配置名拿过来重新配置后,系统就会执行定义的这个函数,配置项在dev.py里:JWT_AUTH
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id':user.id,
        'username':user.username
    }


# 自定义需要使用手机号也可以登录
# 重写默认的登陆方法,原理跟自定义登录后需要返回user_id,username(不只是token)一样
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        判断用户名(手机号)或者密码是否正确，返回对应的用户对象。
        """
        query_set = User.objects.filter(Q(username=username) | Q(mobile=username))
        try:
            if query_set.exists():
                user = query_set.get()  # 取出唯一的一条数据（取不到或者有多条数据都会出错）
                if user.check_password(password):  # 进入一步判断密码是否正确
                    return user
        except:
            return None