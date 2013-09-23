# -*- coding: utf-8 -*-
from main.models.classifieds import *
from main.models.user import UserProfile
from main.models.locations import City
from main.forms import *
from main.helpers import ucwords
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps

JSON_INDENT = None

#def jsonCountries(request):
#    data = Country.objects.all()
#    data = serializers.serialize("json", data, indent = JSON_INDENT)
#    return HttpResponse(data, mimetype = "application/json")

#def jsonProvinces(request, countryId):
#    data = Province.objects.filter(country = countryId)
#    data = serializers.serialize("json", data, indent = JSON_INDENT)
#    return HttpResponse(data, mimetype = "application/json")

#def jsonCities(request, provinceId):
#    data = City.objects.filter(province = provinceId)
#    data = serializers.serialize("json", data, indent = JSON_INDENT)
#    return HttpResponse(data, mimetype = "application/json")

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


def viewClassified(request):
    classifieds = Classified.objects.all()

    return render_to_response(
        'classifieds/single.html',
        {'classifieds': classifieds}, 
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
                classified.contact_location = City.objects.get(pk = request.POST.get('id_contact_city'))
            except:
                None
            #Validate extension/content-type and resize pictures
            if request.user.is_authenticated():
                classified.user = request.user
            #Save city
            classified.save()
            return HttpResponseRedirect('/')
    else:
        #Populate every user data field
        formset = formset_factory(AddClassifiedForm, extra = 0)
        formset = formset(initial = [
            getDefaultUserData(request)
        ])
    return render_to_response(
        'classifieds/create.html', 
        {
            'formset': formset,
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
