from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

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
            return render(request, 'post_register.html', {
                'title': 'Registration Complete!',
                'message': 'Your student account has been created. Please login.'
            })
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
            return render(request, 'post_register.html', {
                'title': 'Registration Complete!',
                'message': 'Your tutor account has been created. Please login.'
            })
        return render(request, 'register_tutor.html', {'form': form})
    
def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid() and form.process(request):
            print(f"{request.user.username} logged in successfully.")
            return HttpResponse(f"Welcome, {request.user.username}!")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('register/student/')