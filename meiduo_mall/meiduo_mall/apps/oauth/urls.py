from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^qq/authorization/$',views.QQURLView.as_view()) # QQ登录
]