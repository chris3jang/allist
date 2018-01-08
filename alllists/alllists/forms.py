from django import forms
from lists.models import List
from django.forms import ModelForm


#class ListForm(forms.Form):
	#item_title = forms.CharField(label='Item', max_length=100)

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)

class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = ['item_title']
		#fields = ['title', 'completed', 'children']

