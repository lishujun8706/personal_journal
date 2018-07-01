from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from personaljnl_view import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'personaljnl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index,name = 'index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.registerUser, name='registerUser'),
    url(r'^userinfo/$', views.userinfo_list,name='userinfo'),
    url(r'^userinfo_verify/$', views.userinfo_verify,name='userverify'),
    url(r'^userinfo/(?P<pk>[0-9]+)/$', views.user_detail,name='userdetail'),
    url(r'^login_verify/$', views.loginVerify,name='loginverify'),
    url(r'^test_verify/$', views.example_view,name='testverify'),
    url(r'^view/',include('personaljnl_view.urls')),
]

urlpatterns += staticfiles_urlpatterns()