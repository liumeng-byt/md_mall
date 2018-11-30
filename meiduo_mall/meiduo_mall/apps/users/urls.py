from django.conf.urls import url


# from meiduo_mall.apps.users import views
from users import views # 添加了导包路径后可以这样写，这里虽然写的正确，但是系统会画红线，需要吧apps导包路径设置为　Source Root 目录

urlpatterns = [
    url(r'^test/$', views.TestView.as_view()),
    url(r'^test2/$', views.TestView2.as_view()),

]
