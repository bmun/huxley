from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from core.models import *

# Dispatch to the appropriate view per the request.
def dispatch(request, page='welcome'):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context_instance=context)

    try:
        views = {'welcome': welcome,
                 'preferences': preferences,
                 'roster': roster,
                 'attendance': attendance,
                 'help': help,
                 'bugs': bugs}
        
        # Call the appropriate view function from the dictionary.
        return views[page](request, request.user.advisor_profile, context)
    # No such view exists.
    except KeyError:
        return HttpResponseNotFound()
    # The profile doesn't exist, meaning user isn't an advisor.
    except ObjectDoesNotExist:
        return HttpResponse(status=403)


# Display and/or edit the advisor's profile information.
def welcome(request, profile, context):
    school = profile.school
    if request.method == 'GET':
        return render_to_response('welcome.html',
                                  {'school': school},
                                  context_instance=context)
    elif request.method == 'POST':
        # TODO (wchieng): refactor this into a Django form.
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name = request.POST.get('lastname')
        request.user.save();
        school.name = request.POST.get('schoolname')
        school.address = request.POST.get('address')
        school.city = request.POST.get('city')
        school.zip = request.POST.get('zip')
        school.programtype = request.POST.get('programtype')
        school.timesattended = request.POST.get('attendance')
        school.primaryname = request.POST.get('primaryname')
        school.primaryemail = request.POST.get('primaryemail')
        school.primaryphone = request.POST.get('primaryphone')
        school.secondaryname = request.POST.get('secname')
        school.secondaryemail = request.POST.get('secemail')
        school.secondaryphone = request.POST.get('secphone')
        school.mindelegationsize = request.POST.get('minDel')
        school.maxdelegationsize = request.POST.get('maxDel')
        school.save();
        
        return HttpResponse(status=200)
        


# Display and/or update the advisor's country/committee preferences.
def preferences(request, profile, context):
    school = profile.school
    countries = Country.objects.filter(special=False).order_by('name')
    countryprefs = school.countrypreferences.all() \
                         .order_by("countrypreference__rank")
    
    # Split the committees into pairs for double-columning in the template.
    committees = Committee.objects.filter(special=True)
    committees = [committees[i:i+2] for i in range(0, len(committees), 2)]
    committeeprefs = school.committeepreferences.all()
    return render_to_response('preferences.html',
                              {'countryprefs': countryprefs,
                               'countries': countries,
                               'committees': committees,
                               'committeeprefs':committeeprefs},
                              context_instance=context)


# Display the advisor's editable roster.
def roster(request, profile, context):
    if request.method == 'GET':
        school = profile.school
        slots = DelegateSlot.objects.filter(assignment__school=school)
        return render_to_response('roster_edit.html',
                                  {'slots': slots},
                                  context_instance=context)
    elif request.method == 'POST':
        # TODO (kmeht): Create the roster update view.
        return HttpResponse(status=200)


# Display the advisor's attendance list.
def attendance(request, profile, context):
    return render_to_response('comingsoon.html')


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