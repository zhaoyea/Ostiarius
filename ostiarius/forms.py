from django import forms
from django.contrib.auth.models import User

from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['asset_no', 'item_name']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']