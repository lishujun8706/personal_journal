from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^login/$',views.login,name = 'user_login'),
    url(r'^userinfo/$',views.userinfo_list),
    url(r'^userinfo/(?P<pk>[0-9]+)/$',views.user_detail),
]