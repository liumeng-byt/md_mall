from rest_framework import serializers
from rest_framework.serializers import Serializer

from oauth.utils import check_encrypted_openid
from users.models import User


class QQUserSerializer(Serializer):
    """绑定openid与美多商城用户的序列化器
    只用到校验功能,没用到序列化的功能

    校验参数:
    mobile,password,sms_code,openid
    """
    openid = serializers.CharField(label='openid',write_only=True)
    mobile = serializers.RegexField(label='手机号',regex=r'^1[3-9]\d{9}$',write_only=True)
    password = serializers.CharField(label='密码',max_length=20,min_length=8, write_only=True)
    sms_code = serializers.CharField(label='短信验证码',write_only=True)

    # 校验参数
    def validate(self, attrs):
        # 获取请求参数
        openid = attrs.get('openid')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        sms_code = attrs.get('sms_code')

        # 校验 openid
        # 获取openid, 校验openid是否有效
        openid = check_encrypted_openid(openid)
        if not openid:
            raise serializers.ValidationError({'message': '无效的openid'})

        # 修改字典中openid的值， 以便保存正确的openid到映射表
        attrs['openid'] = openid

            # 校验短信验证码
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('sms_codes')
        real_sms_code = redis_conn.get('sms_%s' % mobile) # 根据手机号拿到内存中的验证码
        if not real_sms_code:
            raise serializers.ValidationError({"message":"短信验证码无效"})
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError({'message': '短信验证码错误'})

        # 到数据库查询有没有这个手机号
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 没有该手机号,则自动新增为美多用户在进行绑定
            user = User.objects.create_user(
                username = mobile,
                password = password,
                mobile = mobile
            )
        else:
            # 如果数据库里有这个手机号,则校验密码是否正确
            if not user.check_password(password):
                raise serializers.ValidationError({"message":"密码错误"})

        # 将认证后的user放进校验字典中,绑定关联时用到
        attrs['user'] = user

        # 返回校验后的参数
        return attrs

    def create(self, validated_data): # validated_data 返回的校验后的 attrs
        # 获取校验的用户
        user = validated_data.get('user')  # attrs['user'] = user
        openid = validated_data.get('openid')

        # 绑定openid和美多用户:新增一条数据
        from oauth.models import OAuthQQUser
        OAuthQQUser.objects.create(user=user,
                                   openid=openid
                                   )
        return user # 返回的user对象给前面的user = serializer.save() 接收






















