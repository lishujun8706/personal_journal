from django.contrib.auth.models import AbstractUser,User
from django.conf import settings
from rest_framework import serializers
from django.db import models
import datetime

# Create your models here.
class UserInfo(AbstractUser):
    # user_name = models.CharField(null=False,default='Eva_Wall_E',max_length=20,db_index=True)
    # user_password = models.CharField(null=False,max_length=32)
    user_portrait = models.CharField(null=False,default='',max_length=36)
    user_stylesign = models.TextField(null=False,default='')
    user_birthday = models.DateField(null=False)#,default=datetime.date.today())
    user_gender = models.SmallIntegerField(choices=((1,"female"),(2,"male")))
    user_addr = models.CharField(max_length=100, default='', verbose_name='address')
    user_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='mobile_number')

    class Meta:
        verbose_name = 'user_infor_table'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username','password','user_phone','user_addr','user_birthday')

class UserInfoSerializerVerify(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username','password')

class RelationFriend(models.Model):
    user_id = models.ForeignKey(UserInfo,related_name="userinfo2userid")
    friend_id = models.ForeignKey(UserInfo,related_name="userinfo2friend")
    class Meta:
        unique_together = ('user_id', 'friend_id')

class JournalContent(models.Model):
    user_id = models.ForeignKey(UserInfo,related_name="userinfo2journal")
    journal_content = models.TextField(null=False,default='')
    journal_share = models.BooleanField(null=False,default=False)
    future_plan = models.BooleanField(null=False,default=False)
    journal_data = models.DateTimeField(null=False)#,default=datetime.date.today())
