# -*- coding: utf-8 -*-
#TODO inspect and clean these imports
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
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login as originalLogin
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
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
                'id': getattr(city, 'id'),
                'name': u'%s - %s - %s' % (
                    city.name.title(),
                    city.province.name.title(),
                    city.province.country.name.title(),
                )
            }
            list.append(data)
    return HttpResponse(dumps(list), mimetype = 'application/json')

@csrf_exempt
def listClassifieds(request):
    #TODO   Solve the problem with paginator and post filter vars
    search_form = SerarchForm(request.POST)
    advanced_search_form = AdvancedSerarchForm(request.POST)
    if request.POST:
        search_query = Search.prepareClassifiedQuery(request)
        try:
            classifieds = Classified.objects.filter(search_query)[:settings.CLASSIFIED_LIST_MAX_ITEMS_QUERY]
        except:
            Logger.getInstance().error('Invalid parameters at query: <<%s>>' % str(search_query))
            raise Exception('Invalid parameters')
    else:
        classifieds = Classified.objects.all()[:settings.CLASSIFIED_LIST_MAX_ITEMS_QUERY]

    paginator = Paginator(classifieds, settings.CLASSIFIED_LIST_MAX_ITEMS_PER_PAGE)
    try:
        classifieds = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        classifieds = paginator.page(1)
    except EmptyPage:
        classifieds = paginator.page(paginator.num_pages)
     
    return render_to_response(
        'classifieds/list.html',
        {
            'classifieds': classifieds,
            'search_form': search_form,
            'advanced_search_form': advanced_search_form
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

def login(request, template_name = 'registration/login.html',
          redirect_field_name = REDIRECT_FIELD_NAME,
          authentication_form = AuthenticationForm,
          current_app = None, extra_context = None):
    if request.POST and request.POST.get('username'):
        try:
            validate_email(request.POST.get('username'))
            user = UserProfile.objects.get(email = request.POST.get('username'))
            if user:
                request.POST = request.POST.copy()
                request.POST['username'] = user.username
        except:
            pass
    return originalLogin(request, template_name,
          redirect_field_name, authentication_form,
          current_app, extra_context)

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
        {
            'formset': formset
        }, 
        context_instance = RequestContext(request)
    )

@login_required
def myProfile(request):
    user = UserProfile.objects.get(pk = request.user.id)
    if request.method == 'POST':
        formset = EditProfileForm(request.POST, instance = user)
        if formset.is_valid():
            userprofile = formset.save(commit = False)
            try:
                user.city = City.objects.get(pk = request.POST.get('city_id'))
            except:
                pass
            userprofile.save()
            return HttpResponseRedirect('/')
    else:
        formset = EditProfileForm(instance = user, initial = getDefaultUserData(request))
    return render_to_response(
        'registration/profile.html', 
        {
            'formset': formset
        }, 
        context_instance = RequestContext(request)
    )

@login_required
def myClassifieds(request):
    classifieds = Classified.objects.filter(Q(user = request.user.id) | Q(contact_email = request.user.email))
    paginator = Paginator(classifieds, settings.CLASSIFIED_LIST_MAX_ITEMS_PER_PAGE)
    try:
        classifieds = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        classifieds = paginator.page(1)
    except EmptyPage:
        classifieds = paginator.page(paginator.num_pages)
    return render_to_response(
        'classifieds/myclassifieds.html', 
        {
            'classifieds': classifieds
        }, 
        context_instance = RequestContext(request)
    )

@login_required
def deleteClassified(request, classifiedId):
    classified = Classified.objects.get(pk = classifiedId)

    allowed = True
    if not classified.user and not classified.contact_email and not request.user:
        allowed = False
    elif request.user != classified.user and request.user.email != classified.contact_email:
        allowed = False
    if not allowed:
        raise Exception('AccessDenied')

    if request.method == 'POST':
        classified.delete()
        return HttpResponseRedirect('/')

    return render_to_response(
        'classifieds/delete.html', 
        {
            'classified': classified
        }, 
        context_instance = RequestContext(request)
    )

@login_required
def editClassified(request, classifiedId):
    classified = Classified.objects.get(pk = classifiedId)

    allowed = True
    if not classified.user and not classified.contact_email and not request.user:
        allowed = False
    elif request.user != classified.user and request.user.email != classified.contact_email:
        allowed = False
    if not allowed:
        raise Exception('AccessDenied')

    if request.method == 'POST':
        formset = AddClassifiedForm(request.POST, request.FILES, instance = classified)
        if formset.is_valid():
            classified = formset.save(commit = False)
            try:
                classified.city = City.objects.get(pk = request.POST.get('city_id'))
            except:
                pass
            classified.save()
            Upload.generateClassifiedThumbsByRequest(request, classified)
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm(
            instance = classified,
            initial = getClassifiedExtraData(classified)
        )
    return render_to_response(
        'classifieds/create.html', 
        {
            'formset': formset,
        }, 
        context_instance = RequestContext(request)
    )

def addClassified(request):
    if request.method == 'POST':
        formset = AddClassifiedForm(request.POST, request.FILES)
        if formset.is_valid():
            classified = formset.save(commit = False)
            try:
                classified.city = City.objects.get(pk = request.POST.get('city_id'))
            except:
                pass
            if request.user.is_authenticated():
                classified.user = request.user
            else:
                try:
                    classified.user = User.objects.get(email = request.POST.get('contact_email'))
                except:
                    pass
            classified.save()
            Upload.generateClassifiedThumbsByRequest(request, classified)
            #Email.sendClassifiedCreationEmail(classified)
            return HttpResponseRedirect('/')
    else:
        formset = AddClassifiedForm(
            initial = getDefaultUserData(request)
        )
    return render_to_response(
        'classifieds/create.html', 
        {
            'formset': formset,
        }, 
        context_instance = RequestContext(request)
    )

def getDefaultUserData(request):
    userData = {}
    if request.user.id:
        user =  UserProfile.objects.get(pk = request.user.id)
        userData =  {
            'contact_name': user.first_name,
            'contact_email': user.email,
            'contact_phone': user.phone,
        }
        if user.city:
            userData.update({
                'city': user.city.name.title(),
                'city_id': user.city.id,
            })
    return userData

def getClassifiedExtraData(classified):
    classifiedData = {}
    if classified.id:
        classifiedData.update({
            'city': classified.city.name.title(),
            'city_id': classified.city.id,
        })
    return classifiedData