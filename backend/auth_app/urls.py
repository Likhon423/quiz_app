from django.urls import path
from .views import StudentRegisterView, TutorRegisterView, loginView, logoutView

urlpatterns = [
    path('register/student/', StudentRegisterView.as_view(), name='register_student'),
    path('register/tutor/', TutorRegisterView.as_view(), name='register_tutor'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]