from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from cms.models import *

# Dispatch to the appropriate view per the request.
def dispatch(request, page="grading"):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context_instance=context)
    
    try:
        views = {'grading': grading,
                 'attendance': attendance,
                 'help': help,
                 'bugs': bugs}
        
        return views[page](request.user.secretariat_profile, context)
    # No such view exists.
    except KeyError:
        return HttpResponseNotFound()
    # The profile doesn't exist, meaning user isn't a chair.
    except ObjectDoesNotExist:
        return HttpResponse(status=403)


# Display the grading page for chairs.
def grading(profile, context):
    return render_to_response('comingsoon.html')


# Display a page allowing the chair to take attendance.
def attendance(profile, context):
    return render_to_response('comingsoon.html')


# Display a FAQ view.
def help(profile, context):
    c = Context()
    questions = {}
    for cat in HelpCategory.objects.all():
        questions[cat.name] = HelpQuestion.objects.filter(category=cat)
    c.update({"categories": questions})
    return render_to_response('help.html', c, context_instance=context)


# Display a bug-reporting view.
def bugs(profile, context):
    return render_to_response('bugs.html', context_instance=context)