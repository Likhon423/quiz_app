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

    form = QuestionForm()

    if request.method == 'POST':
        question_keys = [key for key in request.POST.keys() if key.startswith('question_text_')]
        num_questions = len(question_keys)

        for i in range(num_questions):
            data = {
                'question_text': request.POST.get(f'question_text_{i}').strip(),
                'question_type': request.POST.get(f'question_type_{i}').strip(),
            }

            question_form = QuestionForm(data)

            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

                if question.is_mcq:
                    correct_option = request.POST.get(f'correct_option_{i}')
                                    
                    option_texts = [
                        request.POST.get(f'option{i}_1').strip(),
                        request.POST.get(f'option{i}_2').strip(),
                        request.POST.get(f'option{i}_3').strip(),
                        request.POST.get(f'option{i}_4').strip(),
                    ]

                    option_index = 1

                    for text in option_texts:
                        if text:
                            option = Option.objects.create(question=question, text=text)
                            if str(option_index) == correct_option:
                                question.correct_answer = text
                        option_index += 1
                    question.save()

                elif question.is_fill_in_blank:
                    blank_value = request.POST.get(f'blank_word_{i}').strip()
                    index_str, blank_word = blank_value.split('|')
                    index = int(index_str)

                    words = list(re.finditer(r"\b[\w']+\b", question.question_text))
                    start, end = words[index].span()
                    updated_text = question.question_text[:start] + "_____" + question.question_text[end:]

                    question.question_text = updated_text
                    question.correct_answer = blank_word
                    question.save()

        return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'add_question.html', {
        'quiz': quiz,
        'question_form': form,
    })