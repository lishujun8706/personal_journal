from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(r'^login/$','personaljnl_view.views.login',name = 'user_login'),
)