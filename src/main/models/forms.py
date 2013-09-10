from django.forms import ModelForm
from main.models.classifieds import Classified
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models.user import User

class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified



class UserCreationForms(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User