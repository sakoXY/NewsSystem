# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'x59Y2T1qyTp7v6KxZxxy59dkqtV4kiEwxpm6Uj0Z'
secret_key = 'tanANVKmzfAa9Xx9pvx5TMM8wm2EfiS5u0Lt5r0e'


def image_store(image_data):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'xiayao'

    # 上传后保存的文件名，如果不指定，那么名字由七牛云维护
    key = None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './picture/22.png'

    ret, info = put_data(token, key, image_data)

    # 处理上传的结果，然后上传成功返回图片名称，否则返回None
    if info.status_code == 200:
        return ret.get("key")
    else:
        return None


# 用来测试图片上传的
if __name__ == '__main__':
    # 使用with测试，可以自动关闭流
    with open("./picture/33.jpg", 'rb') as f:
        image_store(f.read())
