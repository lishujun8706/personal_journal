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
from .models import UserInfoSerializer,UserInfoSerializerVerify

from rest_framework import authentication
from rest_framework import exceptions

from rest_framework.authentication import SessionAuthentication, BasicAuthentication,get_authorization_header
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes

# sys.path.append("..//")
from tools import get_md5

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q,Count
from django.contrib.auth import get_user_model
from .self_forms import registform

import json
import datetime

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


class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

@api_view(['GET'])
@authentication_classes((SessionAuthentication,BasicAuthentication))
@permission_classes((IsAuthenticated,))
def example_view(request,format=None):
    print("RRRRRRRRRRR")
    content={
        'user':unicode(request.user),
        'auth':unicode(request.auth),
    }
    print("=======>")
    print content
    return HttpResponse(json.dumps(content))

def login_view(request):
    print("dddddd")
    return render(request,"personalview/submit.html",)

@csrf_exempt
def loginVerify(request):
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get('password',None)
        print("WWWWWWWWWWWW")
        print username,password
        user = authenticate(username=username,password=password)
        if user is not None:
            print"HHHHHHHHH"
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({'username**':user.username,'userpassowrd':user.password,}))
            else:
                return HttpResponse(json.dumps({'mesg':'username password error'}))
        else:
            print "PPPPPPPPPPPPPPPPPPP"
            user = UserInfo.objects.create_user(username=username, password=password,\
                                                  user_gender=1,user_phone='18914955682',user_birthday=datetime.date.today())
            login(request, user)
            print user
            return render(request,'personalview/reverse.html')
            # return HttpResponse(json.dumps({'mesg': 'new add user'}))
        
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
@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication,BasicAuthentication))
@permission_classes((IsAuthenticated,))
def userinfo_verify(request):
    if request.method == 'GET':
        user = UserInfo.objects.values('username','password').annotate(ttCount=Count('*'))
        #user = UserInfo.objects.all()
        serializer = UserInfoSerializerVerify(user,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializerVerify(data=data)
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
