from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect

from p.judge.helpers import *
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
  if sid=='':
    namespace_parent = None
  else:
    namespace_parent = get_object_or_404(Namespace, id=sid)
  dic = {
    'user': request.user,
    'namespace_parent_list': get_parent_list(namespace_parent),
    'namespace_list': Namespace.objects.filter(parent=namespace_parent),
    'problem_list': Problem.objects.filter(namespace=namespace_parent)
  }
  return render(request, 'namespace.html', dictionary=dic)


@login_required
def problem(request, pid, message=''):
  problem = get_object_or_404(Problem, id=pid)
  dic = {
    'user': request.user,
    'problem': problem,
    'namespace_parent_list': get_parent_list(problem.namespace)
  }
  return render(request, 'problem.html', dictionary=dic)


@login_required
def submit(request, pid=''):
  if request.method=='POST':
    # TODO insert submission into the database
    return redirect('problem', pid=request.POST['pid'])
  else:
    if pid=='':
      raise Http404
    dic = {
      'user': request.user,
      'problem': get_object_or_404(Problem, id=pid)
    }
    return render(request, 'submit.html', dictionary=dic)


@login_required
def upload_test(request, pid=''):
  if request.method=='POST':
    return redirect('problem', pid=request.POST['pid'])
  else:
    if pid=='':
      raise Http404
    dic = {
      'user': request.user
    }
    return render(request, 'test_upload.html', dictionary=dic)


