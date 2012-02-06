from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView

from p.judge.forms import *
from p.judge.helpers import *
from p.judge.models import *


class AnnouncementView(ListView):
  model = Announcement

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(AnnouncementView, self).dispatch(*args, **kwargs)


class GradeIndexView(TemplateView):
  template_name = 'judge/grade_index.html'

  def get_context_data(self, *args, **kwargs):
    context = super(GradeIndexView, self).get_context_data(*args, **kwargs)
    context['group_list'] = self.request.user.groups.all()
    return context

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(GradeIndexView, self).dispatch(*args, **kwargs)


""" Will be moved into helpers.py """
def namespace_nest_list(namespace):
  result = [namespace]
  child = []
  for subnamespace in namespace.namespace_set.all():
    child.extend(namespace_nest_list(subnamespace))
  child.extend(namespace.problem_set.all())
  if child:
    result.append(child)
  return result


class GradeView(TemplateView):
  template_name = 'judge/grade.html'

  def get_context_data(self, *args, **kwargs):
    context = super(GradeView, self).get_context_data(*args, **kwargs)
    context['group'] = get_object_or_404(Group, id=context['params']['pk'])
    gd = GradePolicy.objects.filter(group=self.request.user.groups.all())
    context['namespace_problem'] = [item
      for g in gd
        for item in namespace_nest_list(g.namespace.get())
    ]
    """ todo fill grade """
    return context

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(GradeView, self).dispatch(*args, **kwargs)


class LinkView(ListView):
  model = Link


class BaseNamespaceView(TemplateView):
  template_name = 'judge/namespace.html'

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(BaseNamespaceView, self).dispatch(*args, **kwargs)


class NamespaceIndexView(BaseNamespaceView):

  def get_context_data(self, *args, **kwargs):
    context = super(NamespaceIndexView, self).get_context_data(*args, **kwargs)
    context['namespace_list'] = visible_namespace_list(self.request.user, Namespace.objects.filter(parent=None))
    context['problem_list'] = permitted_problem_list(self.request.user, Problem.objects.filter(namespace=None))
    return context


class NamespaceView(BaseNamespaceView):

  def get_context_data(self, *args, **kwargs):
    context = super(NamespaceView, self).get_context_data(*args, **kwargs)
    context['namespace'] = get_namespace(self.request.user, context['params']['pk'])
    context['namespace_list'] = visible_namespace_list(self.request.user, context['namespace'].namespace_set.all())
    context['problem_list'] = permitted_problem_list(self.request.user, context['namespace'].problem_set.all())
    return context


class ProblemView(DetailView):
  model = Problem

  def get_context_data(self, *args, **kwargs):
    context = super(ProblemView, self).get_context_data(*args, **kwargs)
    if not problem_permitted(self.request.user, context['problem']):
      raise Http404
    context['namespace'] = context['problem'].namespace
    return context 

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(ProblemView, self).dispatch(*args, **kwargs)


class StatusView(ListView):

  def get_queryset(self):
    return user_time_filter(self.request.user, Status.objects)

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(StatusView, self).dispatch(*args, **kwargs)


@login_required
def submit(request, pid=None):
  if request.method=='POST' and pid is None:
    if request.POST['submit_method']=='textarea':
      submission = Submission(
        problem=get_problem(request.user, request.POST['pid']),
        user=request.user,
        code=request.POST['code']
      )
    elif request.POST['submit_method']=='file':
      pass
    submission.full_clean()
    submission.save()
    return redirect('problem', pid=request.POST['pid'])
  elif request.method=='GET' and pid:
    dic = {
      'problem': get_problem(request.user, pid)
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
      'problem': get_problem(request.user, pid)
    }
    return render(request, 'test_upload.html', dictionary=dic)
  else:
    raise Http404


