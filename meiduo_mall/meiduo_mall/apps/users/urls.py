from django.conf.urls import url


# from meiduo_mall.apps.users import views
# 添加了导包路径后可以这样写，这里虽然写的正确，但是系统会画红线，需要吧apps导包路径设置为　Source Root 目录
from rest_framework.routers import DefaultRouter


from users import views
from users.views import UsernameCountView, MyObtainJSONWebToken, AddressViewSet, BrowseHistoryView
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

    # 判断用户名是否存在
    url(r'^usernames/(?P<username>\w{3,20})/count/$', UsernameCountView.as_view()),

    # 注册用户
    url(r'^users/$',views.CreateUserView.as_view()),
    # 用户中心展示数据
    url(r'^user/$', views.UserDetailView.as_view()),
    # 修改邮箱
    url(r'^email/$', views.EmailView.as_view()),
    # 激活邮箱
    url(r'^email/verification/$', views.VerifyEmailView.as_view()),

    # 登录接口(使用第三方包的视图)
    # url(r'^authorizations/$',obtain_jwt_token) # 直接调用jwt里的登陆视图,但是只返回token一个值

    # 登录接口(使用jwt的视图),因为只返回token一个值,所以需要自定义视图函数返回token,user_id,username
    url(r'authorizations/$',MyObtainJSONWebToken.as_view()),

    # 用户浏览历史记录
    url(r'browse_history/$',BrowseHistoryView.as_view()),



]

# 用户地址管理的试图集(增 删 查 改)
router = DefaultRouter()
router.register(r'addresses', AddressViewSet, base_name='addresses')
urlpatterns += router.urls