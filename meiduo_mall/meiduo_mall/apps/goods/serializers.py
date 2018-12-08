from rest_framework import serializers

from goods.models import GoodsCategory, GoodsChannel, SKU


# 列表页导航
class CategorySerializer(serializers.ModelSerializer):
    """类别序列化器"""

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


# 列表页导航
class ChannelSerializer(serializers.ModelSerializer):
    """ 频道序列化器 """
    category = CategorySerializer()

    class Meta:
        model = GoodsChannel
        fields = ('category', 'url')


# 商品列表数据显示
class SKUSerializer(serializers.ModelSerializer):
    """序列化器输出商品SKU信息"""
    class Meta:
        model = SKU
        fields = ('id','name','price','default_image_url','comments')

