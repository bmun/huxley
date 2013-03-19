from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.utils import simplejson

from huxley.core.models import *

# Dispatch to the appropriate view per the request.
def dispatch(request, page="grading"):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context_instance=context)
    
    try:
        views = {'grading': grading,
                 'attendance': attendance,
                 'rosters': rosters,
                 'help': help,
                 'bugs': bugs}
        
        return views[page](request, request.user.secretariat_profile, context)
    # No such view exists.
    except KeyError:
        return HttpResponseNotFound()
    # The profile doesn't exist, meaning user isn't a chair.
    except SecretariatProfile.DoesNotExist:
        return HttpResponse(status=403)


# Display the grading page for chairs.
def grading(request, profile, context):
    return render_to_response('comingsoon.html')


# Display a page allowing the chair to take attendance.
def attendance(request, profile, context):
    if request.method == "POST":
        delegate_slots = simplejson.loads(request.POST['delegate_slots'])
        for slot_data in delegate_slots:
            slot = DelegateSlot.objects.get(id=slot_data['id'])
            slot.attended_session1 = slot_data['session1']
            slot.attended_session2 = slot_data['session2']
            slot.attended_session3 = slot_data['session3']
            slot.attended_session4 = slot_data['session4']
            slot.save()
        return HttpResponse(status=200)

    delegate_slots = DelegateSlot.objects.filter(assignment__committee=profile.committee).order_by('assignment__country')

    return render_to_response(
        'take_attendance.html',
        {'delegate_slots':delegate_slots, 'committee':profile.committee},
        context_instance=context)


# Display a page allowing the USG/External to view delegate rosters.
def rosters(request, profile, context):
    sid, slots = 0, []
    if 'sid' in request.GET:
        sid = request.GET['sid']
        school = School.objects.get(id=sid)
        slots = DelegateSlot.objects.filter(assignment__school=school)
    context.update({
        'sid': sid,
        'schools' : School.objects.all().order_by('name'),
        'delegates' : [slot.delegate for slot in slots]
    })
    return render_to_response('rosters.html', context_instance=context)


# Display a FAQ view.
def help(request, profile, context):
    c = Context()
    questions = {}
    for cat in HelpCategory.objects.all():
        questions[cat.name] = HelpQuestion.objects.filter(category=cat)
    c.update({"categories": questions})
    return render_to_response('help.html', c, context_instance=context)


# Display a bug-reporting view.
def bugs(request, profile, context):
    return render_to_response('bugs.html', context_instance=context)