from django.contrib import admin
from p.judge.models import Announcement, Namespace, Link, Problem, Status


class StatusAdmin(admin.ModelAdmin):
  pass


class AnnouncementAdmin(admin.ModelAdmin):
  list_display = ['title', 'announce_time']
admin.site.register(Announcement, AnnouncementAdmin)


admin.site.register(Namespace)
admin.site.register(Link)
admin.site.register(Problem)
admin.site.register(Status)

