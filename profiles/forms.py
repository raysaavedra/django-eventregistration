from django import forms
from django.forms import ModelForm
from profiles.models import *
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(forms.ModelForm):
    class Meta:
        model = NewUser
        exclude = ('email','first_name','last_name','username','password','is_staff','is_active','is_superuser','last_login','date_joined','user_permissions','groups')

class EventForm(forms.ModelForm):

	class Meta:
		model = Event

class StudentForm(forms.ModelForm):

	class Meta:
		model = Student