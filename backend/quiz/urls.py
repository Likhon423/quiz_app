from django.urls import path
from .views import createQuizView, addQuestionView
from . import api

urlpatterns = [
    path('create/', createQuizView, name='create_quiz'),
    path('<int:quiz_id>/addQuestion/', addQuestionView, name="add_question"),
    path('api/<int:quiz_id>/questions/', api.get_questions, name="get_questions"),
    path('api/<int:quiz_id>/questions/save/', api.save_question, name="save_question"),
    path('api/<int:quiz_id>/questions/update/<int:question_id>/', api.update_question, name="update_question"),
    path('api/<int:quiz_id>/questions/delete/<int:question_id>/', api.delete_question, name="delete_question"),
]