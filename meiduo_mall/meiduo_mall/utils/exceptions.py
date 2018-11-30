from rest_framework.response import Response
from rest_framework.views import exception_handler

import logging
logger = logging.getLogger('django')

def custom_exception_handler(exc, context):
    # 调用DRF的 exception_handler 函数处理异常，如果处理成功，会返回一个`Response`类型的对象
    response = exception_handler(exc, context)

    if response is None: # 表示项目出错了，但DRF框架没有处理
        # 自己处理异常： 获取异常信息并保存到日志文件中
        view = context['view']     # 出错视图
        error = '服务器内部错误： %s，%s' % (view, exc)
        logger.error(error) #　保存出错信息到日志文件中
        return Response({'message': error}, status=500)

    return response