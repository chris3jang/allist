



from django import forms
from lists.models import List
from django.forms import ModelForm


class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = ['item_title']
		#fields = ['title', 'completed', 'children']

