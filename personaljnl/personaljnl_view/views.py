# -*- coding:utf-8 -*-
import os,sys

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .models import UserInfo,JournalContent
from django.template import RequestContext
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .db_serializer import UserInfoSerializer,UserInfoSerializerVerify,JournalContentSerializer

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

def index(request):
    return HttpResponseRedirect(reverse('login'))

def login_view(request,*args,**kwargs):
    print("dddddd")
    return render(request,"personalview/index.html",)

@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication,BasicAuthentication))
@permission_classes((IsAuthenticated,))
def home(request):
    user = request.user
    print user
    print "***********************************"
    user_jurl = JournalContent.objects.filter(user_id=user)
    joural_data = JournalContentSerializer(data=user_jurl)
    return render(request, "personalview/home.html", )
    # if joural_data.is_valid():
    #     return JsonResponse(joural_data.data,status=200)
    # else:
    #     return JsonResponse(joural_data.errors,status=400)

def registerUser(request):
    print request.method
    print request.POST
    print request
    if request.method == "POST":
        email = request.POST.get("email", None)
        username = request.POST.get("username",None)
        password = request.POST.get('password',None)
        phonenumber = request.POST.get('phonenumber', None)
        user = UserInfo.objects.create_user(email=email,username=username, password=password,\
                                              user_gender=1,user_phone=int(phonenumber),user_birthday=datetime.date.today())
        login(request, user)
        print '////////////////////////'
        return JsonResponse({'mesg':'ok','reverse_path':'/view/home/'},status=200)
        # return render(request,'personalview/reverse.html')

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

#@csrf_exempt
def loginVerify(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        username = request.POST.get("username",None)
        password = request.POST.get('password',None)
        print("WWWWWWWWWWWW")
        print username,password
        user = authenticate(username=username,password=password)
        if user is not None:
            print"HHHHHHHHH"
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('login'))
                #,content=json.dumps({'mesg':'username password error','code':1})
        else:
            print u"用户不存在，请先注册"
            return HttpResponseRedirect(reverse('login'))
            #,content=json.dumps({'mesg':'username password error','code':1})


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
