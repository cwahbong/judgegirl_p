from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from datetime import datetime

from p.judge.models import Namespace, Problem, Status

def get_parent_list(namespace):
  result = []
  if namespace:
    result.append(namespace)
    while result[-1].parent:
      result.append(result[-1].parent)
    result.reverse()
  return result

def permit_time_check(user, queryset):
  queryset = queryset.filter(status_type='PERMIT')
  queryset = queryset.filter(Q(users=user)|Q(groups=user.groups.all()))
  queryset = queryset.filter(Q(start_time=None)|Q(start_time__lte=datetime.now()))
  queryset = queryset.filter(Q(end_time=None)|Q(end_time__gte=datetime.now()))
  return queryset

def namespace_permitted(user, namespace):
  while namespace:
    namespace_perm = permit_time_check(user, namespace.status_set)
    if namespace_perm:
      return True
    namespace = namespace.parent
  return False

def problem_permitted(user, problem):
  if permit_time_check(user, problem.status_set) or namespace_permitted(user, problem.namespace):
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
  if namespace_permitted(user, namespace):
    return namespace
  else:
    raise Http404

def permitted_problem_list(user, problem_list):
  result = []
  for problem in problem_list:
    if problem_permitted(user, problem):
      result.append(problem)
  return result

def permitted_namespace_list(user, namespace_list):
  result = []
  for namespace in namespace_list:
    if namespace_permitted(user, namespace):
      result.append(namespace)
  return result

