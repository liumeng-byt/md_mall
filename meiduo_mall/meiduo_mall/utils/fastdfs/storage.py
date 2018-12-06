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
        return path