# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.utils import simplejson

from huxley.advisors.decorators import enforce_advisor
from huxley.core.models import *
from huxley.shortcuts import pairwise, render_template


def welcome(request):
    """ Display and/or edit the advisor's profile information. """
    school = request.profile.school
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
        school.zip_code = request.POST.get('zip_code')
        school.program_type = request.POST.get('program_type')
        school.times_attended = request.POST.get('attendance')
        school.primary_name = request.POST.get('primary_name')
        school.primary_email = request.POST.get('primary_email')
        school.primary_phone = request.POST.get('primary_phone')
        school.secondary_name = request.POST.get('secname')
        school.secondary_email = request.POST.get('secemail')
        school.secondary_phone = request.POST.get('secphone')
        school.min_delegation_size = request.POST.get('minDel')
        school.max_delegation_size = request.POST.get('maxDel')
        school.save();
        
        return HttpResponse()    


def preferences(request):
    """ Display and/or update the advisor's country and committee
        preferences. """
    school = request.profile.school

    if request.method == 'POST':
        country_ids = request.POST.getlist('CountryPrefs')
        committee_ids = request.POST.getlist('CommitteePrefs')
        school.refresh_country_preferences(country_ids, shuffled=True)
        school.refresh_committee_preferences(committee_ids)
        
        return HttpResponse()

    # Interleave the country preferences for double-columning in the template.
    countries = Country.objects.filter(special=False).order_by('name')
    ctyprefs = list(school.countrypreferences.all()
                    .order_by("countrypreference__rank"))
    ctyprefs += [None]*(10 - len(ctyprefs)) # Pad the list to length 10.
    countryprefs = [(i+1, ctyprefs[i], ctyprefs[i+5]) for i in range(0, 5)]
    
    # Split the committees into pairs for double-columning in the template.
    committees = pairwise(Committee.objects.filter(special=True))
    committeeprefs = school.committeepreferences.all()
    
    return render_template(request, 'preferences.html',
                           {'countryprefs': countryprefs,
                            'countries': countries,
                            'committees': committees,
                            'committeeprefs':committeeprefs})


def roster(request):
    """ Display the advisor's editable roster, or update information as
        necessary. """
    if request.method == 'POST':
        slot_data = simplejson.loads(request.POST['delegates'])
        for slot_id, delegate_data in slot_data.items():
            slot = DelegateSlot.objects.get(id=slot_id)
            if 'name' in delegate_data and 'email' in delegate_data:
                slot.update_or_create_delegate(delegate_data)
            else:
                slot.delete_delegate_if_exists()

        return HttpResponse()

    school = request.profile.school
    slots = DelegateSlot.objects.filter(assignment__school=school) \
                                .order_by('assignment__committee__name')
    return render_template(request, 'roster_edit.html', {'slots' : slots})


def attendance(request):
    """ Display the advisor's attendance list. """
    delegate_slots = DelegateSlot.objects.filter(
        assignment__school=request.profile.school)
    return render_template(request, 'check-attendance.html',
                           {'delegate_slots': delegate_slots})


def help(request):
    """ Display a FAQ view. """
    questions = {category.name : HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')
