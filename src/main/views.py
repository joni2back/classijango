# -*- coding: utf-8 -*-
from main.models.classifieds import *
from main.models.user import UserProfile
from main.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import json


def logout(request, next_page = '/'):
    auth.logout(request)
    return HttpResponseRedirect(next_page)

def index(request):
    return render_to_response(
        'index.html',
        {}, 
        context_instance = RequestContext(request)
    )

def jsonResponse(request):
    data = serializers.serialize("json", Classified.objects.all(), indent = 4)
    return HttpResponse(data, mimetype = "application/json")

def viewClassified(request):
    classifieds = Classified.objects.all()

    return render_to_response(
        'classified.html',
        {'classifieds': classifieds}, 
        context_instance = RequestContext(request)
    )

def registerUser(request):
    if request.method == 'POST':
        formset = UserRegistrationForm(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = UserRegistrationForm()
    return render_to_response(
        'registration/register.html', 
        {'formset': formset}, 
        context_instance = RequestContext(request)
    )

@login_required
def myProfile(request):
    user = UserProfile.objects.get(pk = request.user.id)

    if request.method == 'POST':
        formset = EditProfileForm(request.POST, instance = user)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = EditProfileForm(instance = user)
    return render_to_response(
        'registration/profile.html', 
        {'formset': formset}, 
        context_instance = RequestContext(request)
    )

def addClassified(request):
    if request.method == 'POST':
        formset = AddClassifiedForm(request.POST, request.FILES)
        if formset.is_valid():
            classified = formset.save(commit = False)
            #Validate extension/content-type and resize pictures
            if request.user.is_authenticated():
                classified.user = request.user
            classified.save()
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm()
    return render_to_response(
        'addclassified.html', 
        {'formset': formset}, 
        context_instance = RequestContext(request))