from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.utils import simplejson

from cms.models import *

import datetime
import sys
import traceback
import re

def login_user(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        error = ""
        
        # Determine if the login is valid.
        if len(username) == 0 or len(password) == 0:
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
        
    return render_to_response('auth.html')


def logout_user(request):
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))


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

def about(request):
        return render_to_response('about.html')