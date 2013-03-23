# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from huxley.core.models import *
from huxley.shortcuts import render_template


def dispatch(request, page='welcome'):
    """ Dispatch to the appropriate view per the request after checking
        for authentication and permissions. """
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context_instance=context)

    views = {'welcome': welcome,
             'preferences': preferences,
             'roster': roster,
             'attendance': attendance,
             'help': help,
             'bugs': bugs}

    try:
        return views[page](request, request.user.advisor_profile, context)
    except KeyError:
        return HttpResponseNotFound()
    except AdvisorProfile.DoesNotExist:
        return HttpResponseForbidden()


def welcome(request, profile, context):
    """ Display and/or edit the advisor's profile information. """
    school = profile.school
    if request.method == 'GET':
        return render_template(request, 'welcome.html', {'school': school})

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


def preferences(request, profile, context):
    """ Display and/or update the advisor's country and committee
        preferences. """
    school = profile.school
    
    if request.method == 'POST':        
        seen = set()
        new_country_ids = []
        for index in range(1, 11):
            country_id = int(request.POST['CountryPref%d' % index])
            if country_id and country_id not in seen:
                new_country_ids.append(country_id)
        
        # Clear and reset country preferences.
        school.countrypreferences.clear()
        for rank, country_id in enumerate(new_country_ids, start=1):
            CountryPreference.objects.create(school=school,
                                             country_id=country_id,
                                             rank=rank)
        
        # Clear and reset committee preferences.
        school.committeepreferences.clear()
        for committee in Committee.objects.filter(special=True):
            if committee.name in request.POST:
                school.committeepreferences.add(committee)
            
        school.save()
        return HttpResponse()

    countries = Country.objects.filter(special=False).order_by('name')
    countryprefs = school.countrypreferences.all() \
                         .order_by("countrypreference__rank")
    
    # Split the committees into pairs for double-columning in the template.
    committees = Committee.objects.filter(special=True)
    committees = [committees[i:i+2] for i in range(0, len(committees), 2)]
    committeeprefs = school.committeepreferences.all()
    return render_template(request, 'preferences.html',
                           {'countryprefs': countryprefs,
                            'countries': countries,
                            'committees': committees,
                            'committeeprefs':committeeprefs})


def roster(request, profile, context):
    """ Display the advisor's editable roster, or update information as
        necessary. """
    if request.method == 'POST':
        slot_data = simplejson.loads(request.POST['delegates'])
        for slot_id, delegate_data in slot_data.items():
            slot = DelegateSlot.objects.get(id=slot_id)
            if 'name' in delegate_data and 'email' in delegate_data:
                try:
                    delegate = slot.delegate
                    delegate.name = delegate_data['name']
                    delegate.email = delegate_data['email']
                    delegate.save()
                except Delegate.DoesNotExist:
                    Delegate.objects.create(name=delegate_data['name'],
                                            email=delegate_data['email'],
                                            delegateslot=slot)
            else:
                try:
                    slot.delegate.delete()
                except:
                    pass

        return HttpResponse()

    slots = DelegateSlot.objects.filter(assignment__school=profile.school) \
                                .order_by('assignment__committee__name')
    return render_template(request, 'roster_edit.html', {'slots' : slots})


def attendance(request, profile, context):
    """ Display the advisor's attendance list. """
    delegate_slots = DelegateSlot.objects.filter(
        assignment__school=profile.school
    )
    return render_template(request, 'check-attendance.html',
                           {'delegate_slots': delegate_slots})


def help(request, profile, context):
    """ Display a FAQ view. """
    questions = {category.name : HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request, profile, context):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')