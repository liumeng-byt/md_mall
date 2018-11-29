from django.conf.urls import url


from meiduo_mall.apps.users import views

urlpatterns = [
    url(r'^test/$', views.TestView.as_view()),

]
