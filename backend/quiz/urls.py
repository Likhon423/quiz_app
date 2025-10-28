from django.urls import path
from .views import createQuizView, addQuestionView

urlpatterns = [
    path('create/', createQuizView, name='create_quiz'),
    path('<int:quiz_id>/addQuestion/', addQuestionView, name="add_question"),
]