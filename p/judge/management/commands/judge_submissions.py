from django.core.management.base import BaseCommand, CommandError
from p.judge.models import Problem, Submission, TestData

class Command(BaseCommand):
  args = ''
  help = 'Judge all of the submitted submissions'

  def handle(self, *args, **kwargs):
    # for submission in submissions:
    # judge it
    pass

