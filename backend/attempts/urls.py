from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>/', views.quiz_attempt_view, name='quiz_attempt'),
    path('<int:attempt_id>/question/', views.get_question, name='get_question'),
    path('<int:attempt_id>/save-answer/', views.save_answer, name='save_answer'),
    path('<int:attempt_id>/navigate/', views.navigate_question, name='navigate_question'),
    path('<int:attempt_id>/submit/', views.submit_attempt, name='submit_attempt'),
    path('my-attempts/', views.my_attempts_view, name='my_attempts'),
    path('<int:attempt_id>/continue/', views.continue_attempt, name='continue_attempt'),
    path('<int:attempt_id>/results/', views.view_results, name='view_results'),
]
