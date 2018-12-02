from django.shortcuts import render
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User
from users.serializers import CreateUserSerializer


# 添加测试类，返回　test.html
class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


# test2/测试类
class TestView2(APIView):
    def get(self, request):
        response = Response({'message': 'get请求１'})
        # 在响应头里添加数据，解决跨域请求的问题，允许8080端口的前端页面跨域访问
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return response

    def post(self, request):
        response = Response({'message': 'post请求２'})
        # 在响应头里添加数据，解决跨域请求的问题，允许8080端口的前端页面跨域访问
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return response


"""
response对象

{
  status: 200,
  data: {
     user_id: 10,
     username: 'python'
  },
  headers: {}
}

// 取值
response.status
response.data.user_id
response.data.username

"""
"""
error对象
var error = {
    message : "Request failed with status code 500",
    response : {
        status : 500,
        data : {
            detail: "请求超过了限速。 Expected available in 56 seconds.",
            username: ["仅允许5-20个字符的用户名" ],
            non_field_errors: ['短信验证码不正确']
        }
        headers : {}
    }
}

// 取值
error.response.data.detail
error.response.data.username[0]
error.response.data.non_field_errors[0]

"""


# 判断用户名是否存在
class UsernameCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # print(count)
        data = {
            "username": username,
            "count": count
        }
        return Response(data)


# 用户注册视图
class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer


# 登陆接口
class MyObtainJSONWebToken(ObtainJSONWebToken):
    pass
    # 登录接口(使用jwt的视图),因为只返回token一个值,所以需要自定义视图函数返回token,user_id,username
    # 要返回的token,user_id,username,被定义users/utils.py,不在使用继承的类的返回值

    # 用手机号也可以登录的方法定义在users/utils.py,不在使用继承的类的只允许用户名登录