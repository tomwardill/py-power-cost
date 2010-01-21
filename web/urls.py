from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from app import views

urlpatterns = patterns('',
    # Example:
    # (r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', views.default,
        name='app-default'),
    url(r'^upload/$', views.upload,
        name='app-upload'),
    url(r'^raw/$', views.raw_view,
        name='app-raw'),
    url(r'^bulk_upload/$', views.bulk_upload,
        name='app-bulk_upload'),

    url(r'^hour/$', views.hour,
        name='app-hour'),
    url(r'^day/$', views.day,
        name='app-day'),
    url(r'^week/$', views.week,
        name='app-week'),
    url(r'^month/$', views.month,
        name='app-month'),
    url(r'^all_time/$', views.all_time,
        name='app-all_time'),

    url(r'^data/hour/$', views.data_hour,
        name='app-data_hour'),
    url(r'^data/day/$', views.data_day,
        name='app-data_day'),
    url(r'^data/week/$', views.data_week,
        name='app-data_week'),
    url(r'^data/month/$', views.data_month,
        name='app-data_month'),
    url(r'^data/all_time/$', views.data_all_time,
        name='app-data_all_time'),
    
)

# Debug pattern for serving media
# ------------------------------------------------
if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
