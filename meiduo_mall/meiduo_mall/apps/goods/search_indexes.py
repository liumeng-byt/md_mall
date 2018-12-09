from haystack import indexes

from goods.models import SKU


# SKU索引类
class SKUIndex(indexes.SearchIndex,indexes.Indexable):
    """SKU索引类"""

    # use_template=True表示后续通过模板来指明该字段的索引值可以由哪些数据库模型类字段组成
    # text名字固定,它声明document = True，表示组合字段,表名该字段是主要进行关键字查询的字段
    text = indexes.CharField(document=True,use_template=True)

    # 保存在索引库中的字段
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True) # 是否上架销售