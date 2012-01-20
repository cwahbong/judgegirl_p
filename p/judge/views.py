from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.template import RequestContext

from django.http import HttpResponse

from p.judge.models import *

def link(request):
  dic = {
    'user': request.user,
    'link_list': Link.objects.all()
  }
  return render(request, 'link.html', dictionary=dic)

@login_required
def announcement(request):
  dic = {
    'user': request.user,
    'announce_list': Announcement.objects.all().order_by('-announce_time')
  }
  return render(request, 'announcement.html', dictionary=dic)

@login_required
def namespace(request, sid=''):
  """ TODO find the current namespace
  """
  try:
    dic = {
      'user': request.user,
      'namespace_parent_list': []
    }
    namespace_parent = None
    if sid!='':
      namespace_parent = Namespace.objects.get(id=sid)
      dic['namespace_parent_list'].append(namespace_parent)
      while dic['namespace_parent_list'][-1].parent:
        dic['namespace_parent_list'].append(dic['namespace_parent_list'][-1].parent)
      dic['namespace_parent_list'].reverse()
    dic['namespace_list'] = Namespace.objects.filter(parent=namespace_parent)
    dic['problem_list'] = Problem.objects.filter(namespace=namespace_parent)
    return render(request, 'namespace.html', dictionary=dic)
  except Namespace.DoesNotExist:
    raise Http404


@login_required
def problem(request, pid):
  try:
    dic = {
      'user': request.user,
      'problem': Problem.objects.get(id__exact=pid)
    }
    return render(request, 'problem.html', dictionary=dic)
  except Problem.DoesNotExist:
    raise Http404

@login_required
def submit(request, pid):
  pass
#  try:
#    dic = {
#      'user': request.user
#      'problem': Problem.objects.get(id__exact=pid)
#    }
#    return render(request, 'submit.html', dictionary=dic)
#  except Problem.DoesNoeExist:
#    raise Http404

@login_required
def upload_test(request):
  pass

