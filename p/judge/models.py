from django.db import models, IntegrityError
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime

class Announcement(models.Model):
  """ Represents an announcement.  The last modify time will be
      filled automatically.
  """
  title = models.CharField(max_length=256)
  content = models.TextField()
  announce_time = models.DateTimeField(editable=False)

  class Meta:
    ordering = ['-announce_time']

  def clean(self, *args, **kwargs):
    self.announce_time = datetime.now()
    super(Announcement, self).clean(*args, **kwargs)

  def __unicode__(self):
    return self.title + ' (' + unicode(self.announce_time) + ')'


class Link(models.Model):
  """ Represents the hyperlink.

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


class Namespace(models.Model):
  """ Represents an namespace. The namespace with different parent
      namespace can have same name.

      The namespace N will be visible when any of its children is visible
      in order to visit its children (namespace of problem).  It this
      situation you can only see the visible children of the namespace N.
  """
  parent = models.ForeignKey('self', blank=True, null=True, default='', on_delete=models.CASCADE)
  name = models.CharField(
    max_length=256,
    validators=[
      RegexValidator(regex='^\w+$', message='Enter a valid value, it should only contain alnum and underscore.'),
    ]
  )

  class Meta:
    unique_together = ('parent', 'name')
    ordering = ['name']

  def clean(self, *args, **kwargs):
    if self.parent==self:
      raise ValidationError('Parent cannot be self.')
    if self.parent==None and Namespace.objects.filter(parent=None).filter(name=self.name):
      raise ValidationError('The name of the Namespace with the same Parent already exists.')
    super(Namespace, self).clean(*args, **kwargs)

  def parent_list(self):
    p = self
    result = []
    while p:
      result.append(p)
      p = p.parent
    result.reverse()
    return result

  def __unicode__(self):
    if self.parent and self.parent.name!='':
      return unicode(self.parent) + '::' + self.name
    else:
      return self.name


class Problem(models.Model):
  """ Represents the problem.  The problem can be at exactly one
      namespace ('None' means the root namespace).

      We suggest you put some problems in the same namespace, then you
      can change the permission of them together.
  """
  namespace = models.ForeignKey('Namespace', blank=True, null=True, on_delete=models.PROTECT)
  time_limit = models.IntegerField()          # Unit: second
  memory_limit = models.IntegerField()        # Unit: MB
  output_limit = models.IntegerField()        # Unit: MB
  input_file = models.CharField(max_length=256, blank=True, null=True, default=None)    # leave blank to use stdin
  output_file = models.CharField(max_length=256, blank=True, null=True, default=None)   # leave blank to use stdout
  title = models.CharField(max_length=256)
  main_description = models.TextField()
  input_description = models.TextField()
  output_description = models.TextField()
  sample_input = models.TextField()
  sample_output = models.TextField()
  test_data = models.ManyToManyField('TestData', blank=True)
  is_submittable = models.BooleanField(default=True)
  is_test_uploadable = models.BooleanField(default=False)

  def __unicode__(self):
    if self.namespace:
      return unicode(self.namespace) + '::' + self.title
    else:
      return '::' + self.title


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
      ('SILENCE', 'silence')
    )
  )
  start_time = models.DateTimeField(blank=True, null=True, default=None)
  end_time = models.DateTimeField(blank=True, null=True, default=None)
  description = models.TextField(blank=True, null=True, default=None)
  
  class Meta:
    verbose_name_plural = 'Statuses'

  def __unicode__(self):
    return self.description


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
  submit_time = models.DateTimeField(editable=False)
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

  def clean(self, *args, **kwargs):
    self.submit_time = datetime.now()
    self.request_time = self.submit_time
    super(Submission, self).clean(*args, **kwargs)

  def __unicode__(self):
    return 'Problem: ' + unicode(self.problem) + " User: " + unicode(self.user) + " Time: " + unicode(self.submit_time)


class TestData(models.Model):
  """ under construction
  """
  submit_user = models.ForeignKey(User, null=True, default=None, editable=False)
  usable_problem = models.ForeignKey('Problem', null=True)
  input = models.TextField()
  output = models.TextField()


