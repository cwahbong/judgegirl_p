from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from p.judge.views import *

admin.autodiscover() # enable the admin

urlpatterns = patterns('',
  
  url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}, name='index'),
  url(r'^announcement/$', AnnouncementView.as_view(), name='announcement'),
  url(r'^namespace/$', NamespaceView.as_view(), name='namespace'),
  url(r'^namespace/(?P<pk>\d+)/$', NamespaceView.as_view(), name='namespace'),
  url(r'^problem/(?P<pk>\d+)/$', ProblemView.as_view(), name='problem'),
  url(r'^status/$', StatusView.as_view(), name='status'),
  url(r'^submit/$', 'p.judge.views.submit', name='submit'),
  url(r'^submit/(?P<pid>\d+)/$', 'p.judge.views.submit', name='submit'),
  url(r'^upload_test/$', 'p.judge.views.upload_test', name='upload_test'),
  url(r'^upload_test/(?P<pid>\d+)/$', 'p.judge.views.upload_test', name='upload_test'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
  url(r'^link/$', LinkView.as_view(), name='link'),
  
  url(r'^admin/', include(admin.site.urls)) # enable admin
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')) # enable documentation
)

