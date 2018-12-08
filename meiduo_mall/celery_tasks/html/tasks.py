import os

from django.conf import settings
from django.template import loader

from celery_tasks.main import celery_app
from contents.crons import get_categories


@celery_app.task(name='generate_static_list_search_html')
def generate_static_list_search_html():
    """生成静态的商品列表页和搜索结果页html文件"""
    print('admin后台改动后自动调用generate_static_list_search_html()重新生成静态商品列表list(没有用到定时,位置:html.tasks)')
    # 商品分类菜单
    categories = get_categories()

    # 渲染模板,生成静态html文件
    context = {
        'categories':categories,
    }

    template = loader.get_template('list.html')
    html_text = template.render(context) # 生成静态化的list.html

    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'list.html')
    with open(file_path,'w') as f:
        f.write(html_text)
