from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages

from .forms import RegisterForm, LoginForm

class StudentRegisterView(views.View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register_student.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'student'
            user.save()
            messages.success(request, 'Student account created successfully! Please log in.')
            return redirect('login')
        return render(request, 'register_student.html', {'form': form})
    
class TutorRegisterView(views.View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register_tutor.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'tutor'
            user.save()
            messages.success(request, 'Tutor account created successfully! Please log in.')
            return redirect('login')
        return render(request, 'register_tutor.html', {'form': form})
    
def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid() and form.process(request):
            print(f"{request.user.username} logged in successfully.")
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('login')