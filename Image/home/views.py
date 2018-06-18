# coding=utf-8
import numpy as np
import cv2
import json
from django.db import connection, transaction
from django.core import serializers
from matplotlib import pyplot as plt
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from home.models import User,Shares,Likes
import time


# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()
    headImg = forms.FileField()


def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            # 写入数据库
            user = User()
            user.username = username
            user.headImg = headImg
            user.password = password
            user.email = email
            user.save()
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render_to_response('register.html', {'uf': uf})


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()



def login(request):
    if request.method == "POST":
        uf = LoginForm(request.POST)
        if uf.is_valid():
            user = User.objects.get(email=uf.cleaned_data['email'])
            if user.password == uf.cleaned_data['password']:
                sql="SELECT headImg FROM home_user WHERE user_id = "+str(user.user_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                userheadImg = cursor.fetchone()
                response={'success':1,'user_id':user.user_id,'username':user.username,'head_img':userheadImg[0],'email':user.email}
                return HttpResponse(json.dumps(response))
            else:
                response = {'success': 0}
                return HttpResponse(json.dumps(response))
    else:
        uf = LoginForm()
    return render_to_response('login.html', {'uf': uf})


class PostForm(forms.Form):
    user_id = forms.IntegerField()
    img = forms.FileField()

def share(request):
    if request.method == "POST":
        uf = PostForm(request.POST, request.FILES)
        if uf.is_valid():
            share = Shares()
            share.user = User.objects.get(user_id=uf.cleaned_data['user_id'])
            share.img = uf.cleaned_data['img']
            share.save()
            return HttpResponse(share.share_id)
    else:
        uf = PostForm()
    return render_to_response('post.html', {'uf': uf})

def post(request):
    if request.method == "POST":
        uf = PostForm(request.POST, request.FILES)
        if uf.is_valid():
            share=Shares()
            share.user=User.objects.get(user_id=uf.cleaned_data['user_id'])
            share.img=uf.cleaned_data['img']
            share.save()
            img_path=share.img.name
            # u=User.object.get(user_id=uf.cleaned_data['user_id'])
            # return HttpResponse(share.share_id+" "+url)

            img = cv2.imread("E:\\py\Image\\"+img_path)
            # img = '../'+img_path
            mask = np.zeros(img.shape[:2], np.uint8)

            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)
            cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img = img * mask2[:, :, np.newaxis]
            img = cv2.merge((img, 255 * mask2))
            file_name = "E:\\py\Image\\"+img_path+'.png'
            cv2.imwrite(file_name, img)

            response = HttpResponse(readFile(file_name), content_type='image/png')
            # response = HttpResponse(img, content_type='image/png')
            response['Content-Disposition'] = 'inline;filename=img.png'
            return response
            # return HttpResponse(img_path)
    else:
        uf = PostForm()
    return render_to_response('post.html', {'uf': uf})

def index(request):
    return HttpResponse('image')


def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()

def allShareList(request):
    from datetime import datetime

    sql="SELECT * FROM home_shares,home_user WHERE home_shares.user_id=home_user.user_id ORDER BY time DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    share_list=[]
    for item in res:
        time=item[1]
        time=time.isoformat()
        share_item={"share_id":item[0],"time":time,"img":item[2],"is_hot":item[3],"like":item[4],"user_id":item[5],"username":item[7],"head_img":item[11]}
        share_list.append(share_item)
    data = json.dumps(share_list)
    return HttpResponse(data)

def hotShareList(request):
    from datetime import datetime

    sql="SELECT * FROM home_shares,home_user WHERE home_shares.user_id=home_user.user_id AND is_hot = '1' ORDER BY time DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    share_list=[]
    for item in res:
        time=item[1]
        time=time.isoformat()
        share_item={"share_id":item[0],"time":time,"img":item[2],"is_hot":item[3],"like":item[4],"user_id":item[5],"username":item[7],"head_img":item[11]}
        share_list.append(share_item)
    data = json.dumps(share_list)

    return HttpResponse(data)

def myShareList(request):
    from datetime import datetime
    import json
    from django.db import connection, transaction
    id=request.GET.get('id')
    sql="SELECT * FROM home_shares,home_user WHERE home_shares.user_id=home_user.user_id AND home_shares.user_id="+id+" ORDER BY time DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    share_list=[]
    for item in res:
        time=item[1]
        time=time.isoformat()
        share_item={"share_id":item[0],"time":time,"img":item[2],"is_hot":item[3],"like":item[4],"user_id":item[5],"username":item[7],"head_img":item[11]}
        share_list.append(share_item)
    data = json.dumps(share_list)

    return HttpResponse(data)