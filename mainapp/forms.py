from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from . import models

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['user']


class CVForm(forms.ModelForm):
    class Meta:
        model = models.CV
        exclude = ['cv', 'ctreation_date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ['parent', 'author', 'post', 'created_at']



