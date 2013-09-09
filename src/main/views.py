from main.models.classifieds import Classified
from main.models.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def viewClassified(request):
    classifieds = Classified.objects.all()

    return render_to_response(
        'classified.html',
        {'classifieds': classifieds}, 
        context_instance = RequestContext(request)
    )



def registerUser(request):
    if request.method=='POST':
        formset = UserCreationForms(request.POST)
        if formset.is_valid:
            formset.save()
            #return HttpResponseRedirect('/register')
    else:
        formset = UserCreationForms()
    return render_to_response(
        'register.html', 
        {'formset': formset}, 
        context_instance=RequestContext(request)
    )



def addClassified(request):
    if request.method=='POST':
        formset = AddClassifiedForm(request.POST)
        if formset.is_valid:
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm()
    return render_to_response(
        'addclassified.html', 
        {'formset': formset}, 
        context_instance = RequestContext(request))

