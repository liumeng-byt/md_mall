from django.conf.urls import url

from carts import views

urlpatterns = [

    url(r'^cart/$',views.CartView.as_view()),
    # 商品全选或全不选
    url(r'^cart/selection/$',views.CartSelectAllView.as_view()),


]