# -*- coding:utf-8 -*-
import os,sys

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .models import UserInfo
from django.template import RequestContext
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfoSerializer

# sys.path.append("..//")
from tools import get_md5

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .self_forms import registform

# 让用户可以用邮箱登录
# setting 里要有对应的配置
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username = username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def login(request):
    print("dddddd")
    return render(request,"personalview/index.html",)

def loginVerify(request):
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get('password',None)
        secretkey = settings.SECRET_KEY
        user = UserInfo.objects.filter(user_name=username)
        if not user:
            #Todo register
            return render(request,'user/register.html',)
        else:
            if password and user.password == get_md5(password + secretkey):
                return render(request,'index.html',)
        
@csrf_exempt
def userinfo_list(request):
    if request.method == 'GET':
        user = UserInfo.objects.all()
        serializer = UserInfoSerializer(user,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
    try:
        user = UserInfo.objects.get(pk=pk)
    except UserInfo.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)