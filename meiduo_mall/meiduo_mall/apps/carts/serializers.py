from rest_framework import serializers
from rest_framework.serializers import Serializer
from goods.models import SKU


# 增加/修改 购物车
class CartSerializer(Serializer):
    """增加/修改 购物车序列化器
    请求参数：sku_id count selected
    响应参数：sku_id count selected
    """
    sku_id = serializers.IntegerField(label='sku id',min_value=1)
    count = serializers.IntegerField(label='数量',min_value=1)
    selected = serializers.BooleanField(label='是否勾选',default=True)

    def validate(self, attrs):
        try:
            sku = SKU.objects.get(id=attrs['sku_id'])
        except SKU.DoesNotExist:
            raise serializers.ValidationError("商品不存在")
        return attrs


# 显示 购物车商品数据
class CartSKUSerializer(serializers.ModelSerializer):
    """
    显示 购物车商品数据显示序列化器
    """
    count = serializers.IntegerField(label='数量')
    selected = serializers.BooleanField(label='是否勾选')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image_url', 'price', 'count', 'selected')


# 删除购物车数据
class CartDeleteSerializer(Serializer):
    """删除购物车"""
    sku_id = serializers.IntegerField(label='商品id',min_value=1)

    def validate_sku_id(self,attr):
        try:
            sku = SKU.objects.get(id=attr)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return attr


# 购物车全选
class CartSelectAllSerializer(Serializer):
    """购物车全选"""
    selected = serializers.BooleanField(label='全选')