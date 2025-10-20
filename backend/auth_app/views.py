from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from .forms import RegisterForm
from .models import User

class StudentRegisterView(views.View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register_student.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is None:
                return render(request, 'register_student.html', {'form': form})
            user.role = 'student'
            user.save()
            return render(request, 'post_register.html', {
                'title': 'Registration Complete!',
                'message': 'Your student account has been created. Please login.'
            })
        return render(request, 'register_student.html', {'form': form})
    
class TutorRegisterView(views.View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register_tutor.html', {'form': form, 'for_tutor': True})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is None:
                return render(request, 'register_tutor.html', {'form': form, 'for_tutor': True})
            user.role = 'tutor'
            user.save()
            return render(request, 'post_register.html', {
                'title': 'Registration Complete!',
                'message': 'Your tutor account has been created. Please login.'
            })
        return render(request, 'register_tutor.html', {'form': form, 'for_tutor': True})