from django.conf.urls import url

from goods import views

urlpatterns = [

    # 列表界面导航接口
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryView.as_view()),
    # 查询商品列表数据
    url(r'^skus/$', views.SKUListView.as_view()),

]