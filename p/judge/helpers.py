from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from datetime import datetime

from p.judge.models import Namespace, Problem, Status


def user_time_filter(user, queryset):
  return queryset.filter(Q(users=user)|Q(groups=user.groups.all())
  ).filter(Q(start_time=None)|Q(start_time__lte=datetime.now())
  ).filter(Q(end_time=None)|Q(end_time__gte=datetime.now()))


def namespace_permitted(user, namespace):
  while namespace:
    namespace_perm = user_time_filter(user, namespace.status_set.filter(status_type='PERMIT'))
    if namespace_perm:
      return True
    namespace = namespace.parent
  return False

def namespace_visible(user, namespace):
  if namespace_permitted(user, namespace):
    return True
  for namespace_child in namespace.namespace_set.all():
    if namespace_visible(user, namespace_child):
      return True
  return False

def problem_permitted(user, problem):
  if user_time_filter(user, problem.status_set.filter(status_type='PERMIT')) or namespace_permitted(user, problem.namespace):
    return True
  else:
    return False

def get_problem(user, pid):
  problem = get_object_or_404(Problem, id=pid)
  if problem_permitted(user, problem):
    return problem
  else:
    raise Http404

def get_namespace(user, sid):
  if sid is None:
    return None
  namespace = get_object_or_404(Namespace, id=sid)
  if namespace_visible(user, namespace):
    return namespace
  else:
    raise Http404

def permitted_problem_list(user, problem_list):
  return filter(lambda p: problem_permitted(user, p), problem_list)

def visible_namespace_list(user, namespace_list):
  return filter(lambda n: namespace_permitted(user, n), namespace_list)

