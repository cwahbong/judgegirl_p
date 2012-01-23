from django.contrib import admin
from p.judge.models import Announcement, Namespace, Link, Problem, Status



class AnnouncementAdmin(admin.ModelAdmin):
  list_display = ['title', 'announce_time']

class StatusAdmin(admin.ModelAdmin):
  list_display = ['description', 'start_time', 'end_time']


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Link)
admin.site.register(Namespace)
admin.site.register(Problem)
admin.site.register(Status, StatusAdmin)

