from rest_framework import serializers

from areas.models import Area


# 行政区划序列化器
class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('id','name')

# 子行政区划信息序列化器
class SubAreaSerializer(serializers.ModelSerializer):
    """ 子行政区划信息序列化器 """
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id','name','subs') # Area模型类中中 related_name 的值
