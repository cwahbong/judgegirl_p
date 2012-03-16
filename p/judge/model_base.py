import string

from django.db import models

class AbstractNestedEntry(models.Model):
  """
  This is the base of Namespace and Problem.  It have all of the common
  properties of them.
  """
  parent = models.ForeignKey('Namespace', blank=True, null=True,
    default='', on_delete=models.CASCADE
  )
  name = models.CharField(max_length=255, blank=True, null=True,
    default=''
  )
  weight = models.IntegerField(default=1)

  class Meta:
    abstract = True
    ordering = ['name']
 
  def parent_list(self):
    def parent_iterator(self):
      p = self.parent
      while p:
        yield p
        p = p.parent
    result = list(parent_iterator(self))
    result.reverse()
    return result

  def full_name(self):
    return '{}::{}'.format(
      string.join(map(lambda p: p.name, self.parent_list()), '::'),
      self.name
    )
  
  def __unicode__(self):
    return self.full_name()


class AbstractTestData(models.Model):
  def test_data_namer(instance, filename):
    return instance.__test_data_namer__(filename)
  
  # TODO check if the test data is valid.
  problem = models.ForeignKey('Problem', null=True, default=None,
    on_delete=models.CASCADE
  )
  test_data = models.FileField(upload_to=test_data_namer, null=True,
    default=True
  )

  class Meta:
    abstract = True

  def __unicode__(self):
    return '{} (test data id={})'.format(self.problem, self.id)

