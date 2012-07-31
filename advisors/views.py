from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from cms.models import *

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
        return views[page](request.user.advisor_profile, context)
    # No such view exists.
    except KeyError:
        return HttpResponseNotFound()
    # The profile doesn't exist, meaning user isn't an advisor.
    except ObjectDoesNotExist:
        return HttpResponse(status=403)


# Display and/or edit the advisor's profile information.
def welcome(profile, context):
    school = profile.school
    return render_to_response('welcome.html',
                              {'school': school},
                              context_instance=context)


# Display and/or update the advisor's country/committee preferences.
def preferences(profile, context):
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
def roster(profile, context):
    school = profile.school
    slots = DelegateSlot.objects.filter(assignment__school=school)
    return render_to_response('roster_edit.html',
                              {'slots': slots},
                              context_instance=context)


# Display the advisor's attendance list.
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