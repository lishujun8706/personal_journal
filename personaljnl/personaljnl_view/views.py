import os,sys

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import UserInfo
from django.template import RequestContext
from django.conf import settings

# sys.path.append("..//")
from tools import get_md5

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from models import UserInfo
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
    return render(request,"user/login.html",)

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
        
