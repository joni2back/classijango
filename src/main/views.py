# -*- coding: utf-8 -*-
from main.models.classifieds import Classified
from main.forms import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth


# def loginUser(request):
#     if request.method=='POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/')

#     return render_to_response(
#         'registration/login.html',
#         {'request': request}, 
#         context_instance = RequestContext(request)
#     )

def logout(request, next_page='/'):
    auth.logout(request)
    return HttpResponseRedirect(next_page)


def index(request):
    return render_to_response(
        'index.html',
        {'request': request}, 
        context_instance = RequestContext(request)
    )

def viewClassified(request):
    classifieds = Classified.objects.all()

    return render_to_response(
        'classified.html',
        {'classifieds': classifieds}, 
        context_instance = RequestContext(request)
    )



def registerUser(request):
    if request.method=='POST':
        formset = UserRegistrationForm(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = UserRegistrationForm()
    return render_to_response(
        'register.html', 
        {'formset': formset}, 
        context_instance=RequestContext(request)
    )


def addClassified(request):
    if request.method=='POST':
        formset = AddClassifiedForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm()
    return render_to_response(
        'addclassified.html', 
        {'formset': formset, 'request': request}, 
        context_instance = RequestContext(request))

