from django.forms import ModelForm
from main.models.classifieds import Classified
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified



class UserCreationForms(UserCreationForm):
	email = forms.EmailField()