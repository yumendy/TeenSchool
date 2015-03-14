from django.conf.urls import patterns, include, url
from django.contrib import admin
from sign import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'teenschool.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.default),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/logout/$', views.logout),
    url(r'^addcourse/$', views.addCourse),
    url(r'^courselist/$', views.courseList),
    url(r'^qrcode/$', views.QRCode),
    url(r'^sign/$',views.sign, name = 'sign'),
    url(r'^recordlist/$', views.recordList),
    url(r'^finishlist/$',views.finishList),
)
