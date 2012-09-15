from django import forms
from accounts.forms import RegistrationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import logout, login, authenticate

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            password = new_user.password
            new_user.set_password(password)
            new_user.save()
            user = authenticate(username=new_user.username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render_to_response("register.html", {'form': form}, context_instance=RequestContext(request))
