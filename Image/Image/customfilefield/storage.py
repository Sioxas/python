# -*-coding:utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import os, time, random,string
from random import Random


class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(FileStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime("%Y%m%d%H%M%S")
        str=string.join(random.sample(['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z'], 8)).replace(" ","")
        fn = "IMG_"+fn + "_"+str
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super(FileStorage, self)._save(name, content)



