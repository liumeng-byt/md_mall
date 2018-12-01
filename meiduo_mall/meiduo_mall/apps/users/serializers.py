import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from users.models import User


class CreateUserSerializer(ModelSerializer):
    """注册用户的序列化器"""
    # 1 校验参数
    # 2 序列化新增用户对象 并返回
    # 只用于校验的参数需要指定为只写(数据库里没有):write_only = True
    password2 = serializers.CharField(label='确认密码', max_length=20, min_length=8, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)
    allow = serializers.BooleanField(label='同意用户协议', default=False, write_only=True)


    class Meta:
        model = User # 关联的模型类
        fields = ('id', 'username', 'password', 'mobile',
                  'password2', 'sms_code',  'allow')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }



    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        # 判断两次密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')


        mobile = attrs.get('mobile')

        # todo: 校验短信验证码
        # 获取正确的短信验证码
        from django_redis import get_redis_connection
        strict_redis = get_redis_connection('sms_codes')  # type: StrictRedis
        real_sms_code = strict_redis.get('sms_%s' % mobile)  # bytes

        if not real_sms_code:
            raise ValidationError('短信验证码无效')
        # 获取用户传递过来的短信验证码
        sms_code = attrs.get('sms_code')
        # 比较是否相等
        print(sms_code, real_sms_code)
        if real_sms_code.decode() != sms_code:
            raise ValidationError('短信验证码不正确')

        return attrs




    # 注册 新增一个用户(重写)
    def create(self, validated_data):  # validated_data 校验过后的数
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile'),
        )
        return user