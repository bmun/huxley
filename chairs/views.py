from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.utils import simplejson

from core.models import *

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
        updated_data = simplejson.loads(request.raw_post_data)

        # Now for some security checks... make sure whoever's logged in has permission to make changes
        slots = DelegateSlot.objects.filter(assignment__committee=profile.committee)
        committee_delegates = set()
        for slot in slots:
            committee_delegates.add(slot.delegate)

        for delegate in updated_data['delegates']:
            try:
                delegateid = int(delegate['delegateid'])
                delegate_object = Delegate.objects.get(id=delegateid)

                # Make sure delegate is part of the committee the logged-in person is in charge of
                if delegate_object not in committee_delegates:
                    print "ERROR: CHAIR TRYING TO MODIFY DELEGATES WITHOUT PERMISSION"
                    return HttpResponse(status=403)

                delegate_object.session1 = delegate['sessions']['1']
                delegate_object.session2 = delegate['sessions']['2']
                delegate_object.session3 = delegate['sessions']['3']
                delegate_object.session4 = delegate['sessions']['4']
                delegate_object.save()

            except:
                print "ERROR WHILE TRYING TO TAKE ATTENDANCE"
                return HttpResponse(status=500)

        return HttpResponse(status=200)

    slots = DelegateSlot.objects.filter(assignment__committee=profile.committee)
    delegates = Delegate.objects.filter(
        delegateslot__assignment__committee=profile.committee
    ).order_by('delegateslot__assignment__country')
    delegate_info = []
    for delegate in delegates:
        delegate_info.append({"id":delegate.id, \
                              "name":delegate.name, \
                              "session1":delegate.session1, \
                              "session2":delegate.session2, \
                              "session3":delegate.session3, \
                              "session4":delegate.session4, \
                              "school":delegate.get_school().name})

    return render_to_response('take_attendance.html', {'delegates':delegate_info, 'committee':profile.committee}, context_instance=context)


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