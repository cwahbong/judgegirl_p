from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.decorators.http import require_http_methods

from p.judge.forms import *
from p.judge.helpers import *
from p.judge.models import *


class AnnouncementView(ListView):
  """ The view that gets all of the announcements and passes it to the
      template 'judge/announcement_list.html'.

      This view only accepts GET and HEAD method.  It also requires
      login.
  """
  model = Announcement
  paginate_by = 5 

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(AnnouncementView, self).dispatch(*args, **kwargs)


class GradeIndexView(TemplateView):
  template_name = 'judge/grade_index.html'

  def get_context_data(self, *args, **kwargs):
    context = super(GradeIndexView, self).get_context_data(*args, **kwargs)
    context['graded_list'] = user_time_filter(self.request.user, Status.objects.filter(status_type='GRADED'))
    return context

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(GradeIndexView, self).dispatch(*args, **kwargs)


""" Will be moved into helpers.py """
def namespace_nest_list(namespaces):
  result = []
  for namespace in namespaces:
    child = namespace_nest_list(namespace.namespace_set.all())
    child.extend(namespace.problem_set.all())
    result.append(namespace)
    if child:
      result.append(child)
  return result

def get_grade_detail(user, entry_list, abs_weight=100, root=True):
  def child_score_sum(child):
    return sum(map(lambda e: e['score'], filter(lambda c: isinstance(c, dict), child)))
  def _helper(user, entry_list, abs_weight=100, root=True):
    result = []
    s = sum(map(lambda e: e.weight, entry_list))
    for entry in entry_list:
      result.append({
        'name': entry.name,
        'ratio': float(abs_weight * entry.weight)/s,
        'score': 0.0
      })
      if isinstance(entry, Namespace):
        child = _helper(
          user,
          list(entry.namespace_set.all())+list(entry.problem_set.all()),
          abs_weight=result[-1]['ratio'],
          root=False
        )
        result[-1]['score'] = child_score_sum(child)
        if child:
          result.append(child)
      elif isinstance(entry, Problem):
        result[-1]['score'] = 1 # TODO query!   (...)*result[-1]['ratio']/full_score
    if root:
      result = [{'name': 'all', 'ratio': abs_weight, 'score': child_score_sum(result)}, result]
    return result
  def _mapper(item):
    if isinstance(item, list):
      return map(_mapper, item)
    else:
      return '{1:04.1f} - {0} - ({2:04.1f}%)'.format(item['name'], item['score'], item['ratio'])
  return map(_mapper, _helper(user, entry_list, abs_weight))
   

class GradeView(TemplateView):
  template_name = 'judge/grade.html'

  def get_context_data(self, *args, **kwargs):
    context = super(GradeView, self).get_context_data(*args, **kwargs)
    context['status_grade'] = get_object_or_404(Status, id=context['params']['pk'])
    gd = Status.objects.filter(status_type='GRADED', groups=self.request.user.groups.all())
    context['namespace_problem'] = get_grade_detail(self.request.user, [n for g in gd for n in g.namespaces.all()])
    """ TODO fill grade by query the submissions """
    return context

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(GradeView, self).dispatch(*args, **kwargs)


class LinkView(ListView):
  """ The view that gets all of the links and passes it to the
      template 'judge/link_list.html'.

      This view only accepts GET and HEAD method.  It does not require
      login.
  """
  model = Link

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  def dispatch(self, *args, **kwargs):
    return super(LinkView, self).dispatch(*args, **kwargs)


class BaseNamespaceView(TemplateView):
  """ We need this base because we need to process the root namespace
      as special case.

      The view only accepts GET and HEAD method.  It requires login.
  """
  template_name = 'judge/namespace.html'

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(BaseNamespaceView, self).dispatch(*args, **kwargs)


class NamespaceIndexView(BaseNamespaceView):
  """ The view to pass the data of the root namespace to template
      (decided in the class BaseNamespaceView).
  """

  def get_context_data(self, *args, **kwargs):
    context = super(NamespaceIndexView, self).get_context_data(*args, **kwargs)
    context['namespace_list'] = visible_namespace_list(self.request.user, Namespace.objects.filter(parent=None))
    context['problem_list'] = permitted_problem_list(self.request.user, Problem.objects.filter(parent=None))
    return context


class NamespaceView(BaseNamespaceView):
  """ The view to pass the data of the non-root namespace to template
      (decided in the class BaseNamespaceView).
  """

  def get_context_data(self, *args, **kwargs):
    context = super(NamespaceView, self).get_context_data(*args, **kwargs)
    context['object'] = get_namespace(self.request.user, context['params']['pk'])
    context['namespace_list'] = visible_namespace_list(self.request.user, context['object'].namespace_set.all())
    context['problem_list'] = permitted_problem_list(self.request.user, context['object'].problem_set.all())
    return context


class ProblemView(DetailView):
  """ The view to pass the data of the problem to template
      'judge/problem_detail.html'.
  """
  model = Problem

  def get_context_data(self, *args, **kwargs):
    context = super(ProblemView, self).get_context_data(*args, **kwargs)
    if not problem_permitted(self.request.user, context['object']):
      raise Http404
    return context 

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(ProblemView, self).dispatch(*args, **kwargs)


class StatusView(ListView):
  """ The view to pass the data of the status of the user to
      template 'judge/status_list.html'.

      It will only get the status that is activated on the user.
  """
  def get_queryset(self):
    return user_time_filter(self.request.user, Status.objects)

  @method_decorator(require_http_methods(["GET", "HEAD"]))
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(StatusView, self).dispatch(*args, **kwargs)

@require_http_methods(["GET", "HEAD", "POST"])
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


@require_http_methods(["GET", "HEAD", "POST"])
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


