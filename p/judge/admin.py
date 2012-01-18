from django.contrib import admin
from p.judge.models import Announcement, Namespace, Problem, Link


admin.site.register(Announcement)
admin.site.register(Namespace)
admin.site.register(Problem)
admin.site.register(Link)

