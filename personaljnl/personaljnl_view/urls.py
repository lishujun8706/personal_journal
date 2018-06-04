from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^login/$',views.login_view,name = 'user_login'),
    url(r'^userinfo/$',views.userinfo_list),
    url(r'^userinfo/(?P<pk>[0-9]+)/$',views.user_detail),
    url(r'^login_verify/$',views.loginVerify),
    url(r'^test_verify/$',views.example_view),
]