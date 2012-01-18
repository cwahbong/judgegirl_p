from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover() # enable the admin

urlpatterns = patterns('',
  
  url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
  url(r'^announcement/$', 'p.judge.views.announcement'),
  url(r'^namespace/$', 'p.judge.views.namespace'),
  url(r'^namespace/(?P<sid>\d+)/$', 'p.judge.views.namespace'),
  url(r'^problem/(?P<pid>\d+)/$', 'p.judge.views.problem'),
  # url(r^submit/', 'judgegirl_p.judge.views.submit'),
  # url(r^testupload/', 'judgegirl_p.judge.views.testupload'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
  url(r'^link/$', 'p.judge.views.link'),
  
  url(r'^admin/', include(admin.site.urls)) # enable admin
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')) # enable documentation
)

