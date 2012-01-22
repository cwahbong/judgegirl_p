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
    'announce_list': Announcement.objects.all()
  }
  return render(request, 'announcement.html', dictionary=dic)


@login_required
def namespace(request, sid=None):
  namespace_parent = get_namespace(sid)
  dic = {
    'user': request.user,
    'namespace_parent_list': get_parent_list(namespace_parent),
    'namespace_list': permitted_namespace_list(Namespace.objects.filter(parent=namespace_parent)),
    'problem_list': permitted_problem_list(Problem.objects.filter(namespace=namespace_parent))
  }
  return render(request, 'namespace.html', dictionary=dic)


@login_required
def problem(request, pid, message=None):
  problem = get_problem(pid)
  dic = {
    'user': request.user,
    'problem': problem,
    'namespace_parent_list': get_parent_list(problem.namespace),
    'message': message
  }
  return render(request, 'problem.html', dictionary=dic)


@login_required
def submit(request, pid=None):
  if request.method=='POST' and pid is None:
    # TODO insert submission into the database
    return redirect('problem', pid=request.POST['pid'])
  elif request.method=='GET' and pid:
    dic = {
      'user': request.user,
      'problem': get_problem(pid)
    }
    return render(request, 'submit.html', dictionary=dic)
  else:
    raise Http404


@login_required
def upload_test(request, pid=None):
  if request.method=='POST' and pid is None:
    # TODO insert testdata into the database
    return redirect('problem', pid=request.POST['pid'])
  elif request.method=='GET' and pid is not None:
    dic = {
      'user': request.user,
      'problem': get_problem(pid)
    }
    return render(request, 'test_upload.html', dictionary=dic)
  else:
    raise Http404


