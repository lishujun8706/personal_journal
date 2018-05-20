from django.db import models
import datetime

# Create your models here.
class UserInfo(models.Model):
    user_name = models.CharField(null=False,default='Eva_Wall_E',max_length=20,db_index=True)
    user_password = models.CharField(null=False,max_length=16)
    user_portrait = models.CharField(null=False,default='',max_length=36)
    user_stylesign = models.TextField(null=False,default='')
    user_birthday = models.DateField(null=False,default=datetime.date.today())
    user_sex = models.SmallIntegerField(choices=((1,"female"),(2,"male")))

class RelationFriend(models.Model):
    user_id = models.ForeignKey(UserInfo)
    friend_id = models.ForeignKey(UserInfo)
    class Meta:
        unique_together = ('user_id', 'friend_id')

class JournalContent(models.Model):
    user_id = models.ForeignKey(UserInfo)
    journal_content = models.TextField(null=False,default='')
    journal_share = models.BooleanField(null=False,default=False)
    future_plan = models.BooleanField(null=False,default=False)
    journal_data = models.DateTimeField(null=False,default=datetime.date.today())
