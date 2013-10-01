# -*- coding: utf-8 -*-
from main.models.classifieds import *
from main.models.user import UserProfile
from main.models.locations import City
from main.forms import *
from main.helpers import *
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps

@csrf_exempt
def jsonCities(request):
    list = []
    if request.method == 'POST':
        cityName = request.POST.get('cityName')
        cities = City.objects.filter(name__istartswith = cityName)[:15]

        for city in cities:
            data = {
                "id": getattr(city, 'id'),
                "name": u"%s - %s - %s" % (
                    ucwords(city.name.lower()),
                    ucwords(city.province.name.lower()),
                    ucwords(city.province.country.name.lower()),
                )
            }
            list.append(data)
    return HttpResponse(dumps(list), mimetype = "application/json")

def listClassifieds(request):
    results = 15
    search_form = SerarchForm()
    if request.GET.get('search'):
        query = request.GET.get('search')
        search_query = Search.get_query(query, ['title', 'content'])
        classifieds = Classified.objects.filter(search_query)[:results]
    else:
        classifieds = Classified.objects.all()[:results]

    for classified in classifieds:
        classified.url = Seo.prepareClassifiedUrl(classified)
    return render_to_response(
        'classifieds/list.html',
        {
            'classifieds': classifieds,
            'search_form': search_form
        }, 
        context_instance = RequestContext(request)
    )

def viewClassified(request, classifiedTitle, classifiedId):
    classified = Classified.objects.get(pk = classifiedId)
    return render_to_response(
        'classifieds/view.html',
        {
            'classified': classified,
        }, 
        context_instance = RequestContext(request)
    )

def logout(request, next_page = '/'):
    auth.logout(request)
    return HttpResponseRedirect(next_page)

def index(request):
    return render_to_response(
        'index.html',
        {}, 
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
            try:
                #Workaround to save the city by ajax helper
                classified.contact_location = City.objects.get(pk = request.POST.get('contact_city_id'))
            except:
                None

            #TODO: Validate extension/content-type and resize the pictures
            if request.user.is_authenticated():
                classified.user = request.user
            classified.save()
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm(
            initial = getDefaultUserData(request)
        )
    return render_to_response(
        'classifieds/create.html', 
        {
            'formset': formset,
            'contact_city': formset,
            'contact_city_id': formset,
        }, 
        context_instance = RequestContext(request)
    )

def getDefaultUserData(request):
    userData = dict(contact_name = '', contact_email = '', contact_phone = '')
    if request.user.id:
        user =  UserProfile.objects.get(pk = request.user.id)
        userData['contact_name'] = user.first_name
        userData['contact_email'] = user.email
        userData['contact_phone'] = user.phone
    return userData