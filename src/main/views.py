from main.models.classifieds import Classified
from main.models.forms import AddClassifiedForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def classified(request):
    classifieds = Classified.objects.all()

    return render_to_response(
        'classified.html',
        {'classifieds': classifieds}, 
        context_instance = RequestContext(request)
    )


def register(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/register')
    else:
        formulario = UserCreationForm()
    return render_to_response(
        'register.html', 
        {'formulario': formulario}, 
        context_instance=RequestContext(request)
    )



def addclassified(request):
    if request.method=='POST':
        formulario = AddClassifiedForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = AddClassifiedForm()
    return render_to_response(
        'addclassified.html', 
        {'formulario': formulario}, 
        context_instance = RequestContext(request))

