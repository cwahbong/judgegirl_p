from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime

class Announcement(models.Model):
  """ Represents an announcement.
      The last modify time will be filled automatically.
  """
  title = models.CharField(max_length=256)
  content = models.TextField()
  announce_time = models.DateTimeField(editable=False)
  
  def clean(self, *args, **kwargs):
    self.announce_time = datetime.now()
    super(Announcement, self).clean(*args, **kwargs)

  def __unicode__(self):
    return self.title + ' (' + str(self.announce_time) + ')'


class Link(models.Model):
  """ Represents the hyperlink at the 'link' page.
  """
  name = models.CharField(max_length=256)
  url = models.URLField()

  def __unicode__(self):
    return self.name


class Namespace(models.Model):
  """ Represents an namespace.  Since django can not support
      multiple column primary key, this model have some issue
      to solve
  """

  class Meta:
    unique_together = ('parent', 'name')

  parent = models.ForeignKey('self', blank=True, null=True, default='', on_delete=models.CASCADE)
  name = models.CharField(
    max_length=64,
    validators=[
      RegexValidator(regex='^\w+$', message='Enter a valid value, it shoule only contain alnum and underscore.'),
    ]
  )

  def clean(self, *args, **kwargs):
    if self.parent==self:
      raise ValidationError('Parent cannot be self.')
    if self.parent==None and Namespace.objects.filter(parent=None).filter(name=self.name):
      raise ValidationError('Namespace with this Parent and Name already exists.')
    super(Namespace, self).clean(*args, **kwargs)
    
  def __unicode__(self):
    if self.parent and self.parent.name!='':
      return self.parent.__unicode__() + '::' + self.name
    else:
      return self.name


class Problem(models.Model):
  namespace = models.ForeignKey(Namespace, blank=True, null=True, on_delete=models.PROTECT)
  time_limit = models.IntegerField()          # Unit: second
  memory_limit = models.IntegerField()        # Unit: MB
  output_limit = models.IntegerField()        # Unit: MB
  title = models.CharField(max_length=256)
  main_description = models.TextField()
  input_description = models.TextField()
  output_description = models.TextField()
  sample_input = models.TextField()
  sample_output = models.TextField()
  is_submittable = models.BooleanField(default=True)
  is_test_uploadable = models.BooleanField()


class Submission(models.Model):
  problem = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
  user = models.ForeignKey(User)
  code = models.TextField()
  submit_time = models.DateTimeField()
  request_time = models.DateTimeField()
  result = models.CharField(max_length=64)
  message = models.CharField(max_length=1024)

  def __unicode__(self):
    return "Problem: " + self.problem + " User: " + self.user + " Time: " + str(self.submit_time)

class TestData(models.Model):
  problem = models.ForeignKey(Problem, null=True)
  # include input and output
  pass


