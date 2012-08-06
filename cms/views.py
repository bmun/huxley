from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from cms.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template import Context, RequestContext
from django.utils import simplejson
from django.core.validators import email_re
from django.core.urlresolvers import reverse

from forms.registration import RegistrationForm

import datetime
import re

# --------------------------
# --- PAGE DISPLAY VIEWS ---
# --------------------------

#@login_required
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

def _is_user_chair(user):
  try:
    return user.secretariat_profile is not None
  except:
    return False

# TODO - fix the redirect to index when there is no error
def login_user(request):
    error = ""
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
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
            response = {"success": False, "error": error }
          elif _is_user_chair(request.user):
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
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.create_user()                    
            new_school = form.create_school()
            form.add_country_preferences(new_school)
            form.add_committee_preferences(new_school)
            form.create_advisor_profile(new_user, new_school)
                        
            return render_to_response('thanks.html', context_instance=RequestContext(request))    
        else:
            print "> ERROR: FORM IS NOT VALID"        
    else:
        # Accessing for the first time
        form = RegistrationForm()

    countries = Country.objects.filter(special=False).order_by('name')
    committees = Committee.objects.filter(special=True)

    return render_to_response('registration.html', 
                                {'form': form, 'state':'', 
                                 'countries': countries,
                                 'committees': committees},
                                context_instance=RequestContext(request))


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

def validate_pass_again(pass1, pass2): # Done
        return pass1 == pass2

def validate_name(name): # Skip
        # Not much to check really, right?
        #I don't think checking that they're all roman alphabet characters is a good idea.
        return len(name) >= 1

def validate_pass(pass1): # Done
        # How strong do you want their passwords to be?
        # Valid symbols: `~!@#$%^&*()-_+=?
        valid_pass = False
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", pass1) is not None:
                valid_pass = True
        
        return (valid_pass and len(pass1) >= 6)

def validate_school_name(sname): # Done
        unique = (len(School.objects.filter(name = sname)) == 0)        
        return (unique and validate_name(sname))

def validate_username(new_user): # Done
    unique = (len(User.objects.filter(username=new_user)) == 0)
    # May only be alphanumeric characters, underscores
    valid_user = False
    if re.match("^[A-Za-z0-9\_]+$", new_user):
        valid_user = True
    return (unique and valid_user and len(new_user) >= 4)

def validate_unique_user(request): # Keep here?
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

def validate_zip(zip): # Done
        #properLen = (len(zip) == 5)
        #return (properLen and zip.isdigit())
        return zip.isdigit()

def validate_email(email): # Done
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

def validate_phone(phoneNum): # Done
        # Format: (123) 456-7890 || Note the space after the area code.
        if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", phoneNum):
                return True
        else:
                return False
def validate_int_phone(phoneNum): # Done 
        if re.match("^[0-9\-x\s\+\(\)]+$", phoneNum):
                return True
        else:
                return False

def validate_number(numString): # Done, I think
        return numString.isdigit()

def validate_programtype(ptype): # Unnecessary
        # Pretty simple
        return (ptype == "class" or ptype == "club")