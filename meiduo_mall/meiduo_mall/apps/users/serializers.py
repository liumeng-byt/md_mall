import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from celery_tasks.email.tasks import send_verify_email
from goods.models import SKU
from users.models import User, Address


# 注册用户的序列化器
class CreateUserSerializer(ModelSerializer):
    """注册用户的序列化器"""
    # 1 校验参数
    # 2 序列化新增用户对象 并返回
    # 只用于校验的参数需要指定为只写(数据库里没有):write_only = True
    password2 = serializers.CharField(label='确认密码', max_length=20, min_length=8, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)
    allow = serializers.BooleanField(label='同意用户协议', default=False, write_only=True)

    # 增加token字段
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        model = User  # 关联的模型类
        fields = ('id', 'username', 'password', 'mobile',
                  'password2', 'sms_code', 'allow', 'token')  # 增加token

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
        # 校验短信验证码
        # 获取正确的短信验证码
        from django_redis import get_redis_connection
        strict_redis = get_redis_connection('sms_codes')
        real_sms_code = strict_redis.get('sms_%s' % mobile)  # bytes

        if not real_sms_code:
            raise ValidationError('短信验证码无效')
        # 获取用户传递过来的短信验证码
        sms_code = attrs.get('sms_code')
        # 比较是否相等

        if real_sms_code.decode() != sms_code:
            raise ValidationError('短信验证码不正确')

        return attrs

    # 注册 新增一个用户(重写)
    def create(self, validated_data):  # validated_data 校验过后的数
       # 保存用户
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile'),
        )

        # 注册成功自动登录，需要生成jwt并返回给客户端
        # 补充生成记录登录状态的token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 生成payload部分的方法(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER # 生成jwt的方法(函数)

        payload = jwt_payload_handler(user) # 生成payload, 得到字典
        token = jwt_encode_handler(payload)  # 生成jwt字符串

        user.token = token  # 生成的jwt 序列化返回

        return user


# 用户中心详细信息序列化器
class UserDetailSerializer(serializers.ModelSerializer):
    """ 用户详细信息序列化器
    仅用于序列化把User里的五个字段展示在用户中心,不做校验
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')



# 修改邮箱序列化器
class EmailSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = User # 指明参照哪个模型类
        fields = ('id','email')  # 指定序列化器中包含哪些字段
        extra_kwargs = {   # 添加或修改原有的选项参数
            'email':{'required':True}  # 请求时,需要传递此参数
        }

    # 修改一条用户数据
    # instance: 要修改的用户对象
    def update(self, instance, validated_data): # instance一个用户对象
        # 保存(修改)邮箱
        email = validated_data['email']
        instance.email = email
        instance.save()

        # 生成邮箱激活链接
        verify_url = instance.generate_verify_email_url()
        # print(verify_url)

        # 发送激活链接到用户邮箱
        send_verify_email.delay(email, verify_url) # email用户邮箱,verify_url邮箱激活链接

        return instance


# 用户地址序列化器
class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器: 序列化 + 校验参数
    """
    province = serializers.StringRelatedField(read_only=True)  # 默认返回关联对象的主键
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    # 新增地址时补充的字段(可读可写)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    def validate_mobile(self, value):
        # 验证手机号
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        """ 保存 """
        # 补充一个字段： 收件地址所属用户, 再保存到数据库表中
        validated_data['user'] = self.context['request'].user  # 获取当前登录用户对象
        # print('self.context', self.context)
        return super().create(validated_data)

    class Meta:
        model = Address
        # 新增地址，不需要用户传递user到服务器，服务器可以自动获取到当前登录用户对象
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')


# 地址标题
class AddressTitleSerializer(serializers.ModelSerializer):
    """地址标题"""
    class Meta:
        model = Address
        fields = ('title',)


# 添加浏览历史序列化器
class AddBrowseHistorySerializer(serializers.Serializer):
    """保存用户浏览记录
        1. 校验商品id
        2. 保存商品id到redis
        3. 序列化
    """
    sku_id = serializers.IntegerField(label='商品sku编号',min_value=1)

    def validate_sku_id(self,value):
        # 检验sku_id是否存在
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('该商品不存在')
        return value

    def create(self, validated_data):
        """保存sku_id到redis中"""
        # 序列化器用于GenericAPIView时，会有一个字典类型的属性叫context，里面包含了request对象
        # history_1 =  [2, 1, 3]

        # 获取sku_id
        sku_id = validated_data.get('sku_id')

        # 获取登陆用户对象
        user_id = self.context.get('request').user.id

        # 获取StrictRedis对象
        strictredis = get_redis_connection('history')  # dev/history

        # 删除商品id
        #  删除全部b：  lrem name 0 b
        strictredis.lrem('history_%s' % user_id,0,sku_id)

        # 把商品id添加到列表左侧
        # 左侧插入：  lpush name liumeng
        strictredis.lpush('history_%s' % user_id,sku_id)

        # 截取列表,控制最多值保存6个元素
        strictredis.ltrim('history_%s' % user_id,0,5)

        # 响应:{"sku_id":1}
        return validated_data