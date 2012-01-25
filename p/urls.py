from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover() # enable the admin

urlpatterns = patterns('',
  
  url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}, name='index'),
  url(r'^announcement/$', 'p.judge.views.announcement', name='announcement'),
  url(r'^namespace/$', 'p.judge.views.namespace', name='namespace'),
  url(r'^namespace/(?P<sid>\d+)/$', 'p.judge.views.namespace', name='namespace'),
  url(r'^problem/(?P<pid>\d+)/$', 'p.judge.views.problem', name='problem'),
  url(r'^status/$', 'p.judge.views.status', name='status'),
  url(r'^submit/$', 'p.judge.views.submit', name='submit'),
  url(r'^submit/(?P<pid>\d+)/$', 'p.judge.views.submit', name='submit'),
  url(r'^upload_test/$', 'p.judge.views.upload_test', name='upload_test'),
  url(r'^upload_test/(?P<pid>\d+)/$', 'p.judge.views.upload_test', name='upload_test'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
  url(r'^link/$', 'p.judge.views.link', name='link'),
  
  url(r'^admin/', include(admin.site.urls)) # enable admin
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')) # enable documentation
)

