import os,sys

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import UserInfo
from django.template import RequestContext
from django.conf import settings

sys.path.append("..//")
from tools import get_md5

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
        
