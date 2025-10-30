from django.urls import path
from .views import create_quiz_view, all_quizzes_view, my_quizzes_view, add_question_view
from . import api

urlpatterns = [
    path('create/', create_quiz_view, name='create_quiz'),
    path('api/<int:quiz_id>/delete/', api.delete_quiz, name='delete_quiz'),
    path('my_quizzes/', my_quizzes_view, name='my_quizzes'),
    path('all_quizzes/', all_quizzes_view, name='all_quizzes'),
    path('<int:quiz_id>/addQuestion/', add_question_view, name="add_question"),
    path('api/<int:quiz_id>/questions/', api.get_questions, name="get_questions"),
    path('api/<int:quiz_id>/questions/save/', api.save_question, name="save_question"),
    path('api/<int:quiz_id>/questions/update/<int:question_id>/', api.update_question, name="update_question"),
    path('api/<int:quiz_id>/questions/delete/<int:question_id>/', api.delete_question, name="delete_question"),
]