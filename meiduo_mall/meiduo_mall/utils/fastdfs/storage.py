from django.conf import settings
from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client


class FdfsStorage(FileSystemStorage):
    """自定义文件存储系统"""
    def _save(self,name,content):
        """当用户通过django管理后台上传文件时,会自动调用此方法保存文件到FastDFS服务器中
        :param name: 传入的文件名
        :param content: Django接收到的文件内容
        :return: 上传文件的路径
        """
        client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        dict_data = client.upload_by_buffer(content.read())

        if 'Upload successed.' != dict_data.get('Status'):
            raise Exception('上传文件到fastDFS失败')

        # 获取文件id
        path = dict_data.get('Remote file_id')

        # Django会将该方法的返回值保存到数据库中对应的文件字段，也就是说该方法应该返回要保存在数据库中的文件名称信息。
        # print(path)  # <fdfs_client.connection.Connection object at 0x7f6d3321f4e0><fdfs_client.fdfs_protol.Tracker_header object at 0x7f6d3321f080>group1/M00/00/02/wKjqjFwJzP6AO206AADlGWI4qmY2183650
        return path

    # 上穿得文件不能预览,原因是没有对应的url和端口,默认返回的是那么name,需要把url加上,如:  'http://image.meiduo.site:8888/'
    def url(self, name):
        """
        返回文件的完整路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        # print(settings.FDFS_URL) # http://image.meiduo.site:8888/
        # print(name)  # group1/M00/00/02/wKjqjFwJzP6AO206AADlGWI4qmY2183650
        return settings.FDFS_URL + name