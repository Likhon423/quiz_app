from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz, Question
from .models import QuizAttempt, AttemptAnswer
from .forms import AttemptAnswerForm


@login_required
def quiz_attempt_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not quiz.questions.exists():
        return render(request, 'attempt.html', {'quiz': quiz, 'attempt': None})

    attempt = QuizAttempt.objects.create(student=request.user, quiz=quiz)
    attempt.current_question = quiz.questions.first()
    attempt.save(update_fields=['current_question'])

    return render(request, 'attempt.html', {'quiz': quiz, 'attempt': attempt})


@login_required
def get_question(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    question = attempt.current_question
    answer_obj, _ = AttemptAnswer.objects.get_or_create(attempt=attempt, question=question)

    return JsonResponse({
        'question_id': question.id,
        'question_text': question.question_text,
        'options': list(question.options.values_list('text', flat=True)) if hasattr(question, 'options') else [],
        'selected_answer': answer_obj.selected_answer or '',
        'is_last': question == attempt.quiz.questions.last(),
    })


@login_required
def save_answer(request, attempt_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    form = AttemptAnswerForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid form data'}, status=400)

    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    question = get_object_or_404(Question, id=form.cleaned_data['question_id'])
    answer_obj, _ = AttemptAnswer.objects.get_or_create(attempt=attempt, question=question)
    answer_obj.selected_answer = form.cleaned_data['selected_answer']
    answer_obj.save()

    return JsonResponse({'success': True})


@login_required
def navigate_question(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    direction = request.GET.get('direction')

    questions = list(attempt.quiz.questions.order_by('id'))
    current_index = questions.index(attempt.current_question)

    if direction == 'next' and current_index + 1 < len(questions):
        attempt.current_question = questions[current_index + 1]
    elif direction == 'prev' and current_index - 1 >= 0:
        attempt.current_question = questions[current_index - 1]

    attempt.save(update_fields=['current_question'])
    return JsonResponse({'success': True})


@login_required
def submit_attempt(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    attempt.calculate_score()
    return JsonResponse({'success': True, 'score': attempt.score})

@login_required
def my_attempts_view(request):
    attempts = QuizAttempt.objects.filter(student=request.user).select_related('quiz').order_by('-id')

    return render(request, 'my_attempts.html', {'attempts': attempts})

@login_required
def continue_attempt(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)

    if attempt.is_submitted:
        return redirect('view_results', attempt_id=attempt.id)
    
    quiz = attempt.quiz

    return render(request, 'attempt.html', {
        'quiz': quiz,
        'attempt': attempt,
    })


@login_required
def view_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)

    if not attempt.is_submitted:
        return redirect('continue_attempt', attempt_id=attempt.id)
    
    answers = AttemptAnswer.objects.filter(attempt=attempt).select_related('question')
    quiz = attempt.quiz

    question_data = []
    for ans in answers:
        question_data.append({
            'question_text': ans.question.question_text,
            'selected_answer': ans.selected_answer or "-",
            'correct_answer': getattr(ans.question, 'correct_answer', None),
            'is_correct': ans.selected_answer == getattr(ans.question, 'correct_answer', None),
        })

    return render(request, 'view_results.html', {
        'quiz': quiz,
        'attempt': attempt,
        'questions': question_data,
    })