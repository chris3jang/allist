from django import forms
from lists.models import Item
from django.forms import ModelForm


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['item_title']
		#fields = ['title', 'completed', 'children']

