from django.conf.urls import url

from areas import views

urlpatterns = [
    # 查询所有省份
    url(r'^areas/$', views.AreaProvinceView.as_view()),
    # 查询一个区域
    url(r'^areas/(?P<pk>\d+)/$', views.SubAreaView.as_view()),
]