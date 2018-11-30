from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    mobile = models.CharField(max_length=11, verbose_name='手机号') # 因为继承的类里没有手机号，所以需要自定义手机号

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name