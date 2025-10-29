import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Quiz, Option
from .forms import QuizForm, QuestionForm


@login_required
def createQuizView(request):
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
def addQuestionView(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)

    return render(request, 'add_question.html', {'quiz': quiz})