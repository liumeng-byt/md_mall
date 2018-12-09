from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from goods import views

urlpatterns = [

    # 列表界面导航接口
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryView.as_view()),
    # 查询商品列表数据
    url(r'^skus/$', views.SKUListView.as_view()),

]

# GET /skus/search/1/    # 查一条
# GET /skus/search/    # 查多条
 # base_name 路由名称(可配可不配,名字随取)
router = DefaultRouter()
router.register('skus/search',views.SKUSearchViewSet,base_name='skus_search')
urlpatterns += router.urls