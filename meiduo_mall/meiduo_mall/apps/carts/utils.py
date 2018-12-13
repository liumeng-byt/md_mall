"""合并cookie中的购物车数据到redis中"""
import base64
import pickle

from django_redis import get_redis_connection

"""只要登陆之后就来调用一下这个函数"""
def merge_cart_cookie_to_redis(request,  response,  user):
    """合并cookie中的购物车数据到redis中,只要登陆之后就来调用一下这个函数,让购物车合并
    request: 请求对象, 用于获取cookie
    response: 响应对象,用于清除cookie
    user: 登录用户, 用于获取用户id

    """
    # 1. 获取cookie数据(base64字符串)
    cookies = request.COOKIES.get('cart')
    # 2. 如果cookie数据为空，则return返回值无需合并购物车数据
    if not cookies:
        return response
    # 3. base64字符串 --> 字典
    cookies_dict = pickle.loads(base64.b64decode(cookies.encode()))
    #    {2: {'count':1, 'selected':False}, 3: {'count':1, 'selected':False}}
    # 4. 获取操作Redis数据库的StrictRedis对象
    redis_conn = get_redis_connection('cart')
    pip = redis_conn.pipeline()
    # 5. 遍历cookies字典，获取: sku_id, count, selected
    for sku_id,dict_count_selected in cookies_dict.items():
        count = dict_count_selected['count']
        selected = dict_count_selected['selected']
        # 合并操作：以cookie中的商品数量覆盖redis中的数量
        pip.hset('cart_%s' % user.id,sku_id,count)
        # 修改商品勾选状态：操作redis的集合，添加或删除商品id
        if selected:
            pip.sadd('cart_selected_%s' % user.id,sku_id)
        else:
            pip.srem('cart_selected_%s' % user.id,sku_id)
    pip.execute()
    # 6. 清除cookie数据
    response.delete_cookie('cart')
    # 7. 返回响应
    return response