from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # Examples:
    # url(r'^$', 'personaljnl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^views/',include('personaljnl_view.urls')),
]

urlpatterns += staticfiles_urlpatterns()