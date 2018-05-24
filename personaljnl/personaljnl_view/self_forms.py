from django import forms
from django.forms import widgets

class registform(froms.Form):
    username = forms.CharField(label='请输入用户名',max_length=64)
    password = widgets.PasswordInput(attrs={"placeholder":"password"})
    email = forms.CharField(label='邮箱')