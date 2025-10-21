from django import forms
from django.db import IntegrityError
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        help_texts = {
            'username': None
        }

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
            self.add_error('username', ValueError('Username is already registered!'))
            return None
        self.save_m2m()
        instance.refresh_from_db()
        return instance

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def process(self, request):
        user = auth.authenticate(request, **self.cleaned_data)
        if user is None:
            self.add_error(None, ValueError("Invalid credentials. Please check your username or password and try again!"))
            return False
        
        auth.login(request, user)
        return True