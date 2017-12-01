from django import forms
from .models import library_profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

class library_sign_up_form(forms.ModelForm):
    class Meta :
        model = library_profile
        widgets = {
            'library_password': forms.PasswordInput(),
        }
        fields = ('library_id','library_password')

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2",)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user
