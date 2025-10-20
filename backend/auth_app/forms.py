from django import forms
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from .models import User
import traceback

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', ValueError('Passwords do not match'))
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        try:
            instance.save()
        except IntegrityError:
            traceback.print_exc()
            self.add_error(None, ValueError('Email or username is already registered!'))
            return None
        self.save_m2m()
        instance.refresh_from_db()
        return instance
