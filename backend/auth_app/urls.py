from django.urls import path
from .views import StudentRegisterView, TutorRegisterView

urlpatterns = [
    path('register/student/', StudentRegisterView.as_view(), name='register_student'),
    path('register/tutor/', TutorRegisterView.as_view(), name='register_tutor'),
]