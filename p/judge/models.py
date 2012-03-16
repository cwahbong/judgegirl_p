from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime

from p.judge.model_base import *


class Announcement(models.Model):
  """
  Represents an announcement.  The last modify time will be filled
  automatically.
  """
  title = models.CharField(max_length=256)
  content = models.TextField()
  announce_time = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-announce_time']

  def __unicode__(self):
    return self.title


class Link(models.Model):
  """
  Represents the hyperlink.

  Note that it will only check the format of the URL.  It will not
  check if the link is valid.
  """
  name = models.CharField(max_length=256)
  url = models.URLField()
  description = models.CharField(max_length=1024, blank=True)

  class Meta:
    ordering = ['name']

  def __unicode__(self):
    return self.name


class Namespace(AbstractNestedEntry):
  """
  Represents an namespace. The namespace with different parent
  namespace can have same name.

  The namespace N will be visible when any of its children is visible
  in order to visit its children (namespace of problem).  It this
  situation you can only see the visible children of the namespace N.
  """

  class Meta:
    unique_together = ('parent', 'name')

  def clean(self):
    # check circular parent
    p = self.parent
    while p:
      if p.id and self.id and p==self:
        raise ValidationError('Circular parent.')
      p = p.parent
    s = Namespace.objects.filter(parent=None)
    # check uniqueness since database treat each NULL as different value
    # but we define each NULL be same here.
    if not self.parent and s.filter(name=self.name) and s.get(name=self.name)!=self:
      raise ValidationError('The name of the Namespace with the same Parent already exists.')
    super(Namespace, self).clean()

  @models.permalink
  def get_absolute_url(self):
    return ('namespace', [unicode(self.id)])


class Problem(AbstractNestedEntry):
  """
  Represents the problem.  The problem can be at exactly one namespace
  ('None' means the root namespace).

  We suggest you put some problems in the same namespace, then you can
  change the permission of them together.
  """
  time_limit = models.IntegerField()          # Unit: second
  memory_limit = models.IntegerField()        # Unit: MB
  output_limit = models.IntegerField()        # Unit: MB
  cooldown = models.IntegerField(blank=True, null=True, default=None)            # Unit: second
  deadline = models.DateTimeField(blank=True, null=True)
  input_file = models.CharField(max_length=256, blank=True, null=True, default=None)    # leave blank to use stdin
  output_file = models.CharField(max_length=256, blank=True, null=True, default=None)   # leave blank to use stdout
  main_description = models.TextField()
  input_description = models.TextField()
  output_description = models.TextField()
  sample_input = models.TextField()
  sample_output = models.TextField()
  submittable = models.BooleanField(default=True)
  test_uploadable = models.BooleanField(default=False)

  @models.permalink
  def get_absolute_url(self):
    return ('problem', [unicode(self.id)])


class Status(models.Model):
  """
  """
  name = models.CharField(max_length=256)
  users = models.ManyToManyField(User, blank=True, null=True, default=None)
  groups = models.ManyToManyField(Group, blank=True, null=True, default=None)
  namespaces = models.ManyToManyField('Namespace', blank=True, null=True, default=None)
  problems = models.ManyToManyField('Problem', blank=True, null=True, default=None)
  status_type = models.CharField(
    max_length = 8,
    choices=(
      ('TAG', 'tag'),
      ('PERMIT', 'permit'),
      ('SILENCE', 'silence'),
      ('GRADED', 'graded')
    )
  )
  start_time = models.DateTimeField(blank=True, null=True, default=None)
  end_time = models.DateTimeField(blank=True, null=True, default=None)
  description = models.TextField(blank=True, null=True, default=None)
  
  class Meta:
    verbose_name_plural = 'Statuses'

  def __unicode__(self):
    return self.name


class Submission(models.Model):
  """ under construction
  """
  problem = models.ForeignKey('Problem', null=True, on_delete=models.SET_NULL)
  user = models.ForeignKey(User)
  priority = models.IntegerField(
    choices=(
      (2, 'Highest'),
      (1, 'High'),
      (0, 'Normal'),
      (-1, 'Low'),
      (-2, 'Lowest'),
    ),
    default=0
  )
  code = models.TextField(blank=True)
  submit_time = models.DateTimeField(auto_now_add=True)
  request_time = models.DateTimeField(editable=False)
  status = models.CharField(
    max_length=2,
    editable=False,
    choices=(
      ('NS', 'New submission'),
      ('JG', 'Judging'),
      ('RJ', 'Rejudging'),
      ('JD', 'Judged')
    ),
    default='NS'
  )
  result = models.CharField(
    max_length=3,
    editable=False,
    choices=(
      ('AC', 'Accepted'),
      ('NA', 'Not accepted'),
      ('WA', 'Wrong answer'),
      ('TLE', 'Time limit exceeded'),
      ('MLE', 'Memory limit exceeded'),
      ('OLE', 'Output limit exceeded'),
      ('RTE', 'Runtime error'),
      ('RF', 'Restricted function'),
      ('CE', 'Compile error'),
      ('SE', 'System error'),
      ('--', '--')
    ),
    default='--'
  )
  result_message = models.TextField(editable=False)

  def clean(self):
    # TODO need to fix the time.
    self.request_time = datetime.now()
    super(Submission, self).clean()

  def __unicode__(self):
    return 'Problem: ' + unicode(self.problem) + " User: " + unicode(self.user) + " Time: " + unicode(self.submit_time)


class SystemTestData(AbstractTestData):
  """
  Represents a test data uploaded by admin, which can not be downloaded
  by users.
  """
  def __test_data_namer__(self, filename):
    return 'private/problems/{}/testdata/{}'.format(
      self.problem.id,
      filename
    )


class UserUploadedTestData(AbstractTestData):
  """
  Represents a test data of a problem uploaded by users, and can be
  downloaded by other users.

  'p' will judge it when it is free.
  """
  user = models.ForeignKey(User, null=True, default=None)

  def __test_data_namer__(self, filename):
    return 'public/users/{}/problems/{}/testdata/{}'.format(
      self.user.id,
      self.problem.id,
      filename
    )

