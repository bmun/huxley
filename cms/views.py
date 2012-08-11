from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.utils import simplejson

from core.models import *

import datetime
import sys
import traceback
import re

# --------------------------
# --- PAGE DISPLAY VIEWS ---
# --------------------------

def register(request):
        c = RequestContext(request, {})
        state = ""
        username = password = ''
        c.update({'state':state})
        c.update({'username':username})
        c.update({'countries': Country.objects.filter(special=False).order_by('name')})
        c.update({'committees': Committee.objects.filter(special=True)})
        c.update({'selectionrange': range(1, 11)})

        if request.POST:
                # TODO: Need to fix names first before using the line below
                # form = RegistrationForm(request.POST)
                
                # Grab registration field values
                fname = request.POST.get('FirstName')           # Validated
                lname = request.POST.get('LastName')            # Validated
                username = request.POST.get('Username')         # Validated
                password = request.POST.get('Password')         # Validated
                pass2 = request.POST.get('Password2')           # Validated
                international = request.POST.get('us_or_int')
                sname = request.POST.get('SchoolName')          # Validated
                sadd = request.POST.get('SchoolAddress')        # Validated
                city = request.POST.get('SchoolCity')           # Validated
                state = request.POST.get('SchoolState')         # Validated
                zip = request.POST.get('SchoolZip')             # Validated
                country = request.POST.get('SchoolCountry')
                pname = request.POST.get('PrimaryName')         # Validated
                pemail = request.POST.get('PrimaryEmail')       # Validated
                pphone = request.POST.get('PrimaryPhone')       # Validated
                secname = request.POST.get('SecondaryName')     # Validated
                semail = request.POST.get('SecondaryEmail')     # Validated
                sphone = request.POST.get('SecondaryPhone')     # Validated
                
                # Program Information
                programtype = request.POST.get('programtype')   # Validated
                howmany = request.POST.get('howmany')           # Validated
                minDel = request.POST.get('MinDelegation')      # Validated
                maxDel = request.POST.get('MaxDelegation')      # Validated
                
                # Country Preferences
                countrypreferenceslist = []
                for num in range(1, 11):
                        prefid = request.POST.get('CountryPref' + str(num))
                        if prefid != "NULL":
                                print prefid
                                print Country.objects.get(id=prefid)

                                countrypreferenceslist.append(Country.objects.get(id=prefid))       

                # Begin Validation
                valid = True
                
                # Validation Checks -----------------------------
                        
                if validate_name(fname):
                        c.update({'fn_val': fname})
                else:
                        valid = False
                        c.update({'fname': True})
                        c.update({'fn_val': fname})
                
                if validate_name(lname):
                        c.update({'ln_val': lname})
                else:
                        valid = False
                        c.update({'lname': True})
                        c.update({'fn_val': fname})
                
                if validate_username(username):
                        c.update({'user_val': username})
                else:
                        valid = False
                        c.update({'v_username': True})
                        c.update({'user_val': username})
                
                if validate_pass(password):
                        c.update({'pass_val': password})
                else:
                        valid = False
                        c.update({'pass1': True})
                        c.update({'pass_val': password})
                
                if validate_pass_again(password, pass2):
                        c.update({'pass2_val': pass2})
                else:
                        valid = False
                        c.update({'pass_again': True})
                        c.update({'pass2_val': pass2})
                
                schoolint = False
                if (international == "us"):
                        c.update({'ctype_check': 'us'})
                else:
                        c.update({'ctype_check': 'international'})
                        schoolint = True
                
                if validate_school_name(sname):
                        c.update({'sname_val': sname})
                else:
                        valid = False
                        c.update({'sname': True})
                        c.update({'sname_val': sname})
                
                if validate_name(sadd):
                        c.update({'sadd_val': sadd})
                else:
                        valid = False
                        c.update({'sadd': True})
                        c.update({'sadd_val': sadd})
                
                if validate_name(city):
                        c.update({'city_val': city})
                else:
                        valid = False
                        c.update({'city': True})
                        c.update({'city_val': city})
                
                if validate_name(state):
                        c.update({'state_val': state})
                else:
                        valid = False
                        c.update({'s_state': True})
                        c.update({'state_val': state})
                
                if validate_zip(zip):
                        c.update({'zip_val': zip})
                else:
                        valid = False
                        c.update({'s_zip': True})
                        c.update({'zip_val': zip})
                        
                if schoolint:
                        if validate_name(country):
                                c.update({'country_val': country})
                        else:
                                valid = False
                                c.update({'s_country': True})
                                c.update({'country_val': country})
                        
                if validate_name(pname):
                        c.update({'pname_val': pname})
                else:
                        valid = False
                        c.update({'pname': True})
                        c.update({'pname_val': pname})
                
                if validate_email(pemail):
                        c.update({'pemail_val': pemail})
                else:
                        valid = False
                        c.update({'v_pemail': True})
                        c.update({'pemail_val': pemail})
                
                if schoolint:
                        if validate_int_phone(pphone):
                                c.update({'pphone': True})
                        else:
                                valid = False
                                c.update({'pphone': True})
                                c.update({'pphone_val': pphone})
                else:
                        if validate_phone(pphone):
                                c.update({'pphone_val': pphone})
                        else:
                                valid = False
                                c.update({'pphone': True})
                                c.update({'pphone_val': pphone})
                
                if (secname != "") or (semail != "") or (sphone != ""):
                        if validate_name(secname):
                                c.update({'secname_val': secname})
                        else:
                                valid = False
                                c.update({'secname': True})
                                c.update({'secname_val': secname})
                        
                        if validate_email(semail):
                                c.update({'semail_val': semail})
                        else:
                                valid = False
                                c.update({'semail': True})
                                c.update({'semail_val': semail})
                        
                        if validate_phone(sphone):
                                c.update({'sphone_val': sphone})
                        else:
                                valid = False
                                c.update({'sphone': True})
                                c.update({'sphone_val': sphone})
                
                if validate_programtype(programtype):
                        if (programtype == "club"):
                                c.update({'ptype_check': 'club'})
                        else:
                                c.update({'ptype_check': 'class'})
                else:
                        c.update({'ptype_check': 'class'})
                        valid = False
                        c.update({'ptype': True})
                
                if validate_number(howmany):
                        c.update({'howmany_val': howmany})
                else:
                        valid = False
                        c.update({'howmany': True})
                        c.update({'howmany_val': howmany})
                
                if validate_number(minDel):
                        c.update({'minDel_val': minDel})
                else:
                        valid = False
                        c.update({'minDel': True})
                        c.update({'minDel_val': minDel})
                
                if validate_number(maxDel):
                        c.update({'maxDel_val': maxDel})
                else:
                        valid = False
                        c.update({'maxDel': True})
                        c.update({'maxDel_val': maxDel})

                
                # Validation Check End ---------------------------
                
                #print valid
                if valid: 
                        # Assuming the user isn't a total dumbass
                        newUser = User.objects.create_user(username, pemail, password)
                        newUser.first_name = fname
                        newUser.last_name = lname
                        newUser.save()
                        
                        newSchool = School.objects.create(name=sname, address=sadd, city=city, state=state, zip=zip, primaryname = pname, primaryemail = pemail, primaryphone = pphone, secondaryname = secname, secondaryemail = semail, secondaryphone = sphone, programtype = programtype, timesattended = howmany, mindelegationsize = minDel, maxdelegationsize = maxDel, international = schoolint)
                        newSchool.save()
                        
                        # Add country preferences
                        print "Country Preferences List: " + str(countrypreferenceslist)
                        for country in countrypreferenceslist:
                                print "Country " + str(country) + " is at index " + str(countrypreferenceslist.index(country))
                                CountryPreference.objects.create(school=newSchool, country=country, rank=countrypreferenceslist.index(country) + 1).save()
                                print "Adding " + str(country) + " to the school's preferences. Current list is " + str(newSchool.countrypreferences.all())
                        
                        # Add committee preferences
                        for committee in Committee.objects.filter(special=True):
                                if committee.name in request.POST:
                                        print "Adding " + committee.name + " to Committee Preferences of school " + newSchool.name
                                        newSchool.committeepreferences.add(committee)
                        newSchool.save()
                        
                        newProfile = AdvisorProfile.objects.create(user=newUser, school=newSchool)
                        newProfile.save()
                        
                        return render_to_response('thanks.html', c)
                else:
                        c.update({'username':username})
                        # Probably because the username field is blank.
                        c.update({'state':"Invalid Fields. Please try again."})
                        return render_to_response('registration.html', c)
                
        else:
                # For GET requests and anything other than POST
                return render_to_response('registration.html', c)


# ---------------------
# --- PAGE UPDATE VIEWS
# ---------------------

def update_prefs(request):
    if request.method == "POST":
        profile = request.user.advisor_profile
        school = profile.school
        prefs = school.countrypreferences.all()
        commprefs = school.committeepreferences.all() 
        committees = Committee.objects.filter(special=True)
        
        cprefs = []
        for index in range(0,10):
            cprefs.append(request.POST.get('CountryPref'+str(index+1)))
        cprefs = filter((lambda p: p != "NULL"), cprefs)

        countrylist = []
        alreadyDone = set();
        for countryid in cprefs:
            if countryid not in alreadyDone:
                alreadyDone.add(countryid)
                countrylist.append(Country.objects.get(id=countryid))
        
        # Delete old prefs and create new ones
        school.countrypreferences.clear()
        print "school prefs:", school.countrypreferences.all()
        for country in countrylist:
            CountryPreference.objects.create(school=school, country=country, rank=countrylist.index(country) + 1).save()
        
        # Deal with committee preferences now
        school.committeepreferences.clear()
        for comm in committees:
            if comm.name in request.POST:
                print "Adding committee:", comm
                school.committeepreferences.add(comm)
            
        school.save()
        print "school prefs:", school.countrypreferences.all()
        print "comm prefs:", school.committeepreferences.all()

    return HttpResponse('')

                        
# ------------------------
# --- HELPER FUNCTIONS ---
# ------------------------

def validate_pass_again(pass1, pass2):
        return pass1 == pass2

def validate_name(name):
        # Not much to check really, right?
        #I don't think checking that they're all roman alphabet characters is a good idea.
        return len(name) >= 1

def validate_pass(pass1):
        # How strong do you want their passwords to be?
        # Valid symbols: `~!@#$%^&*()-_+=?
        valid_pass = False
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", pass1) is not None:
                valid_pass = True
        
        return (valid_pass and len(pass1) >= 6)

def validate_school_name(sname):
        unique = (len(School.objects.filter(name = sname)) == 0)        
        return (unique and validate_name(sname))

def validate_username(new_user):
    unique = (len(User.objects.filter(username=new_user)) == 0)
    # May only be alphanumeric characters, underscores
    valid_user = False
    if re.match("^[A-Za-z0-9\_]+$", new_user):
        valid_user = True
    return (unique and valid_user and len(new_user) >= 4)

def validate_unique_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=406)

def validate_zip(zip):
        #properLen = (len(zip) == 5)
        #return (properLen and zip.isdigit())
        return zip.isdigit()

def validate_email(email):
        # Super LONG regex courtesy of http://www.ex-parrot.com/pdw/Mail-RFC822-Address.html
        # Figure out how to use super long regex later. Here's the naive version for now.
        #if re.match(".+@.+\..+", email):
        #        return True
        #else:
        #        return False
        if email_re.match(email):
            return True
        else:
            return False

def validate_phone(phoneNum):
        # Format: (123) 456-7890 || Note the space after the area code.
        if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", phoneNum):
                return True
        else:
                return False
def validate_int_phone(phoneNum):
        if re.match("^[0-9\-x\s\+\(\)]+$", phoneNum):
                return True
        else:
                return False

def validate_number(numString):
        return numString.isdigit()

def validate_programtype(ptype):
        # Pretty simple
        return (ptype == "class" or ptype == "club")