# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.utils import simplejson

from huxley.core.models import *
from huxley.shortcuts import pairwise, render_template


def welcome(request):
    """ Display and/or edit the advisor's profile information. """
    school = request.user.school
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
    return render_to_response('comingsoon.html')
    school = request.user.school

    if request.method == 'POST':
        country_ids = request.POST.getlist('CountryPrefs')
        committee_ids = request.POST.getlist('CommitteePrefs')
        school.update_country_preferences(country_ids)
        school.update_committee_preferences(committee_ids)
        Conference.auto_country_assign(school)
        return HttpResponse()

    context = {
        'countries': Country.objects.filter(special=False).order_by('name'),
        'countryprefs': CountryPreference.shuffle(school.get_country_preferences()),
        'committees': pairwise(Committee.objects.filter(special=True)),
        'committeeprefs': school.committeepreferences.all()
    }
    
    return render_template(request, 'preferences.html', context)


def roster(request):
    """ Display the advisor's editable roster, or update information as
        necessary. """
    return render_to_response('comingsoon.html')
    school = request.user.school
    if request.method == 'POST':
        slot_data = simplejson.loads(request.POST['delegates'])
        school.update_delegate_slots(slot_data)
        
        return HttpResponse()

    slots = school.get_delegate_slots()
    return render_template(request, 'roster_edit.html', {'slots' : slots})


def attendance(request):
    """ Display the advisor's attendance list. """
    return render_to_response('comingsoon.html')
    context = {'delegate_slots': request.user.school.get_delegate_slots()}
    return render_template(request, 'check-attendance.html', context)


def help(request):
    """ Display a FAQ view. """
    questions = {category.name : HelpQuestion.objects.filter(category=category)
                 for category in HelpCategory.objects.all()}
    return render_template(request, 'help.html', {'categories': questions})


def bugs(request):
    """ Display a bug reporting view. """
    return render_template(request, 'bugs.html')
