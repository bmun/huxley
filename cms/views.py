from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template import Context, RequestContext
from django.utils import simplejson
from django.core.validators import email_re
from django.core.urlresolvers import reverse

from cms.models import *
#from cms.forms.registration import RegistrationForm

import datetime
import re

# --------------------------
# --- PAGE DISPLAY VIEWS ---
# --------------------------

def index(request):
    try:
        if request.user.is_authenticated():
            try:
                if request.user.secretariat_profile is not None:
                    return render_to_response('secretariat_index.html', context_instance = RequestContext(request))
            except:
                if request.user.advisor_profile is not None:
                    sid = request.user.advisor_profile.school.id
                    school = School.objects.get(id=sid)
                    return render_to_response('advisor_index.html', {'school': school}, context_instance = RequestContext(request))
        else:
            return render_to_response('auth.html', context_instance = RequestContext(request))
    except:
        logout(request)
        return render_to_response('auth.html', context_instance = RequestContext(request))


def advisor(request, page="welcome"):
    try:
        if not request.user.is_authenticated():
            return render_to_response('auth.html', context_instance = RequestContext(request))
        try:
            profile = request.user.advisor_profile
        except:
            return HttpResponse(status=403)
        
        sid = profile.school.id
        school = School.objects.get(id=sid)
        countryprefs = school.countrypreferences.all().order_by("countrypreference__rank")
        committeeprefs = school.committeepreferences.all()
        countries = Country.objects.filter(special=False).order_by('name')
        committees = Committee.objects.filter(special=True)

        if page == "welcome":
            return render_to_response('welcome.html', {'school': school}, context_instance = RequestContext(request))
        elif page == "roster":
            slots = DelegateSlot.objects.filter(assignment__school=school)
            return render_to_response('roster_edit.html', {'slots': slots}, context_instance = RequestContext(request))
        elif page == "help":
            c = Context()
            questions = {}
            for cat in HelpCategory.objects.all():
                    questions[cat.name] = HelpQuestion.objects.filter(category=cat)
            c.update({"categories": questions})
            return render_to_response('help.html', c, context_instance = RequestContext(request))
        elif page == "bugs":
            return render_to_response('bugs.html', context_instance = RequestContext(request))
        elif page == "preferences":
            committees = [committees[i:i+2] for i in range(0, len(committees), 2)]
            return render_to_response('preferences.html', {'countryprefs': countryprefs, 'countries': countries, 'committees': committees, 'committeeprefs':committeeprefs}, context_instance = RequestContext(request))
        elif page == "attendance":
            return render_to_response('comingsoon.html')
        else:
            return HttpResponseNotFound()
    except:
        logout(request)
        return render_to_response('auth.html', context_instance = RequestContext(request))


def chair(request, page="grading"):
    try:
        if request.user.is_authenticated():
            try:
                profile = request.user.secretariat_profile
                committee = profile.committee
            except:
                return HttpResponse(status=403)
            
            if page == "attendance":
                return render_to_response('take_attendance.html')
            elif page == "help":
                c = Context()
                questions = {}
                for cat in HelpCategory.objects.all():
                    questions[cat.name] = HelpQuestion.objects.filter(category=cat)
                    c.update({"categories": questions})
                return render_to_response('help.html', c, context_instance = RequestContext(request))
            else:
                return render_to_response('comingsoon.html')
    except:
        logout(request)
        return render_to_response('auth.html', context_instance = RequestContext(request))

# TODO - fix the redirect to index when there is no error
def login_user(request):
    error = ""
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = HuxleyUser.authenticate(username=username, password=password)
        
        if len(username) == 0 or len(password) == 0:
            error = "Woops! One or more of the fields is blank."
        elif user is None:
            error = "Sorry! The login you provided was invalid."
        elif not user.is_active:
            error = "We're sorry, but your account is inactive."
        else:
            login(request, user)
        
        if request.is_ajax():
            if len(error) > 0:
                response = {"success": False, "error": error}
            elif user.is_chair():
                response = {"success": True, "redirect": reverse('chair', args=['grading'])}
            else:
                response = {"success": True, "redirect": reverse('advisor', args=['welcome'])}
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        
    c = RequestContext(request, {'state':error})
    return render_to_response('auth.html', c) if len(error) > 0 else HttpResponseRedirect('/')
            

def logout_user(request):
    logout(request)
    return HttpResponse(reverse('login')) if request.is_ajax() else HttpResponseRedirect('/')
            
                
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


def about(request):
        return render_to_response('about.html')

# ---------------------
# --- PAGE UPDATE VIEWS
# ---------------------

def update_roster(request):
        if(request.method == "POST"):
                operations = simplejson.loads(request.POST.get('ops'))
                for operation in operations:
                        try:
                                if operation['op'] == 'new':
                                        sid = operation['sid']
                                        slot = DelegateSlot.objects.get(id=sid)
                                        Delegate(name="Delegate Name", email="delegate@site.com", delegateslot=slot).save()
                                        print "Created a new delegate!"
                                elif operation['op'] == 'delete':
                                        sid = operation['sid']
                                        DelegateSlot.objects.get(id=sid).delegate.delete()
                                        print "Deleted a delegate!"
                        except:
                                pass
                
        return HttpResponse('')
                
def update_welcome(request):
    if request.method == 'POST':
        profile = request.user.advisor_profile
        school = profile.school
        
        # Actually modify database here:
        # User (Model)
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name = request.POST.get('lastname')
        request.user.save();
        
        # School (Model)
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
        # delegationpaid?
        school.mindelegationsize = request.POST.get('minDel')
        school.maxdelegationsize = request.POST.get('maxDel')
        school.save();
            
    return HttpResponse('')

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
        

def change_password(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(["POST"])
        
    oldpassword = request.POST.get('oldpassword')
    newpassword = request.POST.get('newpassword')
    newpassword2 = request.POST.get('newpassword2')
    
    if not request.user.is_authenticated():
        return HttpResponse(status=401)
    elif not (oldpassword or newpassword or newpassword2):
        return HttpResponse("One or more fields is blank.")
    elif newpassword != newpassword2:
        return HttpResponse("New passwords must match.")
    elif len(newpassword) < 6:
        return HttpResponse("New password must be at least 6 characters long.")
    elif not re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", newpassword):
        return HttpResponse("New password must have only alphanumeric characters and symbols (above letters)")
    elif not request.user.check_password(oldpassword):
        return HttpResponse("Incorrect password.")
    else:
        request.user.set_password(newpassword)
        request.user.save();
        return HttpResponse('OK')
        

def forgot_password(request):
        if request.method == 'POST':
                user = request.POST.get('username')
                input_email = request.POST.get('email')
                
                if len(user) == 0 and len(input_email) == 0:
                        return HttpResponse("You must fill at least one of the fields!")
                
                if len(user) > 0 and len(input_email) > 0:
                        # Double check against database, make sure email matches that username
                        saidUser = None
                        try:
                                saidUser = User.objects.get(username__exact = user)
                        except:
                                return HttpResponse("No such user in the database!")
                                
                        if input_email == saidUser.email:
                                # Email matches user; password reset
                                newPass = User.objects.make_random_password(length = 8,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                                saidUser.set_password(newPass)
                                saidUser.save()
                                saidUser.email_user("BMUN CMS Password Reset", "Your password has been reset to " + newPass + ".", "password@cms.bmun.net")
                                print "Email sent! (Theoretically)"
                        else:
                                return HttpResponse("Email does not match this user in database!")
                                
                else:
                        # If email: grab email and do the password stuffs.
                        if len(input_email) > 0:
                                saidUser = None
                                try:
                                        saidUser = User.objects.get(email = input_email)
                                except:
                                        return HttpResponse("No user matches that email!")
                                
                                # Password Reset
                                newPass = User.objects.make_random_password(length = 8,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                                saidUser.set_password(newPass)
                                saidUser.save()
                                saidUser.email_user("BMUN CMS Password Reset", "Your password has been reset to " + newPass + ".", "password@cms.bmun.net")
                                print "Email sent! (Theoretically)"
                                
                        else:
                                # Else: Check if user is in database first
                                saidUser = None
                                try:
                                        saidUser = User.objects.get(username__exact = user)
                                except:
                                        return HttpResponse("This user doesn't exist!")
                                
                                # Password Reset
                                newPass = User.objects.make_random_password(length = 8,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                                saidUser.set_password(newPass)
                                saidUser.save()
                                saidUser.email_user("BMUN CMS Password Reset", "Your password has been reset to " + newPass + ".", "password@cms.bmun.net")
                                print "Email sent! (Theoretically)"
        else:
                return render_to_response('forgot.html', context_instance = RequestContext(request))
                        
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
        #print "Username",username
        unique = (len(User.objects.filter(username=username)) == 0)
        if unique:
            #print "I'M UNIQUE"
            return HttpResponse(status=200)
        else:
            #print "I'M ORDINARY D:"
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