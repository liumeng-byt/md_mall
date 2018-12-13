from django.conf.urls import url


from orders.views import OrderSettlementView, SaveOrderView

urlpatterns = [
    # # 确认订单
    url(r'^orders/settlement/$',OrderSettlementView.as_view()),
    # 结算订单
    url(r'^orders/$',SaveOrderView.as_view()),




]

