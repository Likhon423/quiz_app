import re
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz
from .forms import QuizForm


@login_required
def create_quiz_view(request):
    if request.user.role != 'tutor':
        return redirect('home')
    
    form = QuizForm()
    
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.tutor = request.user
            quiz.save()
            print(f"Quiz '{quiz.title}' created successfully by {request.user.username}")
            return redirect('add_question', quiz_id = quiz.id)
        return render(request, 'create_quiz.html', {'form': form})
    
    return render(request, 'create_quiz.html', {'form': form})
    

@login_required
def my_quizzes_view(request):
    if request.user.role != 'tutor':
        return redirect('home')
    
    quizzes = Quiz.objects.filter(tutor=request.user).order_by('-created_at')
    return render(request, 'my_quizzes.html', {'quizzes': quizzes})
    
@login_required
def all_quizzes_view(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'all_quizzes.html', {'quizzes': quizzes})

@login_required
def add_question_view(request, quiz_id):
    if request.user.role != 'tutor':
        return redirect('home')
    
    quiz = Quiz.objects.get(id=quiz_id, tutor=request.user)
    return render(request, 'add_question.html', {'quiz': quiz})

