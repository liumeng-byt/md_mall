from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer

from utils.models import BaseModel


class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    mobile = models.CharField(max_length=11, verbose_name='手机号') # 因为继承的类里没有手机号，所以需要自定义手机号

    # 用户中心需要展示
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    # 新增字段： 在用户表新增用户的默认地址
    default_address = models.ForeignKey('Address', related_name='users',
                                        null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name # 复数

    # 生成激活邮件的链接(签名)
    def generate_verify_email_url(self):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY,expires_in=60*60*24) # 秘钥有效期1天
        # 生成token 把token放如链接 #
        token = serializer.dumps({"user_id":self.id,"email":self.email}).decode()
        # 生成链接
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token

        return verify_url


