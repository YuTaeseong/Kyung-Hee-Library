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

    def save(self, commit=True):  # 저장하는 부분 오버라이딩
        user = super(UserCreationForm, self).save(commit=False)  # 본인의 부모를 호출해서 저장하겠다.
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user