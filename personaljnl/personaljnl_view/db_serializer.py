# -*- coding:utf-8 -*-
from rest_framework import serializers
from models import *

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username','password','user_phone','user_addr','user_birthday')

class UserInfoSerializerVerify(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username','password')

class JournalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalContent
        fields = ('journal_content','journal_share','journal_data')