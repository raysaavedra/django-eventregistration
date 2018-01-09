from django import forms
import datetime

class StudentForm(forms.Form):
	barcode = forms.CharField(max_length=30)
	lastname = forms.CharField(max_length=30)