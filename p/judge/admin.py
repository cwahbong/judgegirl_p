from django.contrib import admin
from p.judge.models import Announcement, Namespace, Link, Problem, Status, Submission, TestData



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


class ProblemAdmin(admin.ModelAdmin):
  list_display = ['title', 'namespace', 'time_limit', 'memory_limit', 'output_limit', 'is_submittable', 'is_test_uploadable']
  list_filter = ['is_submittable', 'is_test_uploadable']
  # raw_id_fields = ['namespace']
  filter_horizontal = ['test_data']
  fieldsets = [
    (None, {
      'fields': (
        ('namespace', 'title'),
      )
    }),
    ('Constraints', {
      'fields': (
        ('time_limit', 'output_limit', 'memory_limit'),
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
    ('Test data', {
      'fields': ('test_data',)
    }),
    ('Input/Output', {
      'fields': (('input_file', 'output_file'), ),
      'classes': ['collapse']
    }),
    ('Extra', {
      'fields': (
        ('is_submittable', 'is_test_uploadable'),
      ),
      'classes': ['collapse']
    })
  ]


class StatusAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'start_time', 'end_time']
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
admin.site.register(Link, LinkAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(TestData)

