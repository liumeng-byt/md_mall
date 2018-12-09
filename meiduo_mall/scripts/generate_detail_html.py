import os
import sys
import django


# 终端中运行:ImportError: No module named 'meiduo_mall'
#  需要添加导包路径
sys.path.insert(0,'../')


# python运行报错:raise AppRegistryNotReady("Apps aren't loaded yet.")django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
# 设置配置文件,初始化django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
django.setup()

from celery_tasks.html.tasks import generate_static_sku_detail_html
from goods.models import SKU


if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        print(sku,"(批量生成静态文件脚本, 路径:scripts/)")
        generate_static_sku_detail_html(sku.id)
