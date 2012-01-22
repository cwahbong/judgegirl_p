from django.http import Http404
from django.shortcuts import get_object_or_404

from p.judge.models import Namespace, Problem, Status

def get_parent_list(namespace):
  result = []
  if namespace != None:
    result.append(namespace)
    while result[-1].parent:
      result.append(result[-1].parent)
    result.reverse()
  return result

def get_problem(pid):
  problem = get_object_or_404(Problem, id=pid)
  #all_perm = Status.objects.filter(status_type='permission')
  #prob_perm = all_perm.filter()
  #if 
  #  raise Http403
  return problem

def permitted_problem_list(problem_list):
  return problem_list

def get_namespace(sid):
  if sid is None:
    return None
  namespace = get_object_or_404(Namespace, id=sid)
  return namespace

def permitted_namespace_list(namespace_list):
  return namespace_list

