from django.contrib import admin

from p.judge.models import *


class AnnouncementAdmin(admin.ModelAdmin):
  list_display = ['title', 'announce_time']
  

class LinkAdmin(admin.ModelAdmin):
  list_display = ['name', 'url', 'description']
  fieldsets = [
    (None, {
      'fields': (
        ('name', 'url'),
        'description'
      )
    })
  ]


class SubNamespaceInline(admin.TabularInline):
  model = Namespace
  verbose_name = 'Subnamespace'
  verbose_name_plural = 'Subnamespaces'


class NamespaceAdmin(admin.ModelAdmin):
  search_fields = ['name']
  inlines = [SubNamespaceInline]
  fieldsets = [
    ('Self', {
      'fields': (
        'parent',
        'name'
      )
    })
  ]


class TestDataInline(admin.TabularInline):
  model = TestData
  extra = 0
  verbose_name_plural = 'Test data'
  

class ProblemAdmin(admin.ModelAdmin):
  list_display = ['title', 'namespace', 'deadline', 'cooldown',  'time_limit', 'memory_limit', 'output_limit', 'submittable', 'test_uploadable']
  list_filter = ['submittable', 'test_uploadable']
  inlines = [TestDataInline]
  fieldsets = [
    (None, {
      'fields': (
        ('namespace', 'title'),
      )
    }),
    ('Constraints', {
      'fields': (
        'deadline',
        ('time_limit', 'output_limit', 'memory_limit'),
        ('cooldown')
      )
    }),
    ('Descriptions', {
      'fields': (
        'main_description',
        ('input_description', 'output_description')
      )
    }),
    ('Sample Input/Output', {
      'fields': (
        ('sample_input', 'sample_output')
      ),
      'classes': ['monospace']
    }),
    ('Input/Output file', {
      'fields': (('input_file', 'output_file'), ),
      'classes': ['collapse']
    }),
    ('Extra', {
      'fields': (
        ('submittable', 'test_uploadable'),
      ),
      'classes': ['collapse']
    })
  ]


class StatusAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'start_time', 'end_time']
  list_filter = ['status_type']
  filter_vertical = ['users', 'groups', 'problems', 'namespaces']
  fieldsets = [
    (None, {
      'fields': (
        ('name', 'status_type'),
        'description'
      )
    }),
    ('Duration', {
      'fields': (
        ('start_time', 'end_time'),
      )
    }),
    ('User/Group', {
      'fields': (
        ('users', 'groups'),
      )
    }),
    ('Problem/Namespace', {
      'fields': (
        ('problems', 'namespaces'),
      )
    })
  ]


class SubmissionAdmin(admin.ModelAdmin):
  list_display = ['id', 'problem', 'user', 'priority', 'submit_time', 'status', 'result']
  readonly_fields = ['problem', 'user', 'code']
  fieldsets = [
    (None, {
      'fields': (
        ('problem', 'user'),
        'priority',
        'code'
      )
    })
  ]


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(GradePolicy)
admin.site.register(Link, LinkAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Submission, SubmissionAdmin)
#admin.site.register(TestData)

