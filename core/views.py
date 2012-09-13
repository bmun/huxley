from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from core.models import *
from core.forms.registration import RegistrationForm

import re

# Renders the appropriate base index template.
def index(request):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context)
    elif SecretariatProfile.objects.filter(user=request.user).exists():
        return render_to_response('secretariat_index.html', context)
    else:
        return render_to_response('advisor_index.html', context)


# Logs in a user or renders the login template.
def login_user(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        error = ""
        
        # Determine if the login is valid.
        if not (username and password):
            error = "Woops! One or more of the fields is blank."
        elif user is None:
            error = "Sorry! The login you provided was invalid."
        elif not user.is_active:
            error = "We're sorry, but your account is inactive."
        else:
            login(request, user)
        
        # Determine the appropriate response.
        if request.is_ajax():
            if error:
                response = {"success": False, "error": error}
            elif SecretariatProfile.objects.filter(user=user).exists():
                response = {"success": True,
                            "redirect": reverse('chair', args=['grading'])}
            else:
                response = {"success": True,
                            "redirect": reverse('advisor', args=['welcome'])}
            
            return HttpResponse(simplejson.dumps(response),
                                mimetype='application/json')
        elif error:
            c = RequestContext(request, {'state':error})
            return render_to_response('auth.html', c)
        else:
            return HttpResponseRedirect(reverse('index'))
        
    c = RequestContext(request)
    return render_to_response('auth.html', c)


# Logs out the current user.
def logout_user(request):
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))


# Registers a new user and school
def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.create_user()                    
            new_school = form.create_school()
            form.add_country_preferences(new_school)
            form.add_committee_preferences(new_school)
            form.create_advisor_profile(new_user, new_school)
            
            new_user.email_user("Thanks for registering for BMUN 61!",
                                "We're looking forward to seeing %s at BMUN 61. "
                                "You can find information on deadlines and fees at "
                                "http://bmun.org/bmun/timeline/. If you have any "
                                "more questions, please feel free to email me at "
                                "info@bmun.org. See you soon!\n\nBest,\n\nNishita Agarwal"
                                "\nUSG of External Relations, BMUN 61" % new_school.name,
                                "info@bmun.org")            
            return render_to_response('thanks.html', context_instance=RequestContext(request))    
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


# Attempts to change current user's password.
def change_password(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(["POST"])
        
    oldpass = request.POST.get('oldpassword')
    newpass = request.POST.get('newpassword')
    newpass2 = request.POST.get('newpassword2')
    
    if not request.user.is_authenticated():
        return HttpResponse(status=401)
    elif not (oldpass or newpass or newpass2):
        return HttpResponse("One or more fields is blank.")
    elif newpass != newpass2:
        return HttpResponse("New passwords must match.")
    elif len(newpass) < 6:
        return HttpResponse("New password must be at least 6 characters long.")
    elif not re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", newpass):
        return HttpResponse("New password must have only alphanumeric "
                            "characters and symbols (above letters)")
    elif not request.user.check_password(oldpass):
        return HttpResponse("Incorrect password.")
    else:
        request.user.set_password(newpass)
        request.user.save();
        return HttpResponse('OK')


# Resets a user's password.
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        input_email = request.POST.get('email')
        
        if not (username or input_email):
            return HttpResponse("You must fill at least one of the fields.")
        
        user = None
        try:
            if username and input_email:
                user = User.objects.get(username__exact=username,
                                        email__exact=input_email)
            elif input_email:
                user = User.objects.get(email__exact=input_email)
            else:
                user = User.objects.get(username__exact=username)
        except:
            return HttpResponse("Sorry! We couldn't find a user matching the "
                                "given username and/or email.")
        
        new_pass = User.objects.make_random_password(length=8)
        print new_pass
        print user.email
        user.set_password(new_pass)
        user.save()
        user.email_user("Huxley Password Reset",
                        "Your password has been reset to %s. "
                        "Thanks for using Huxley!" % new_pass,
                        "no-reply@bmun.org")
        return HttpResponse()
    else:
        return render_to_response('forgot.html',
                                  context_instance=RequestContext(request))


# Checks that a username is unique.
def validate_unique_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=406)
        else:
            return HttpResponse(status=200)


# Renders the "About" page.
def about(request):
        return render_to_response('about.html')