from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^home/$',views.home,name = 'home'),
    # url(r'^userinfo/$',views.userinfo_list),
    # url(r'^userinfo_verify/$',views.userinfo_verify),
    # url(r'^userinfo/(?P<pk>[0-9]+)/$',views.user_detail),
    # url(r'^login_verify/$',views.loginVerify),
    # url(r'^test_verify/$',views.example_view),
]