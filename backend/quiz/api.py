import json, re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Quiz, Question, Option
from .forms import QuestionForm



def serialize_question(question):
    return {
        'id': question.id,
        'question_text': question.question_text,
        'question_type': question.question_type,
        'correct_answer': question.correct_answer,
        'options': list(question.options.values_list('text', flat=True)) if question.is_mcq else [],
        'blank_word': question.correct_answer if question.is_fill_in_blank else '',
    }

@login_required
def get_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    questions = quiz.questions.all()
    data = [serialize_question(q) for q in questions]
    return JsonResponse({'question': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    data = json.loads(request.body.decode('utf-8'))

    question_text = data.get('question_text').strip()
    question_type = data.get('question_type').strip()

    if not question_text or not question_type:
        return JsonResponse({'success': False, 'error': 'Missing fields.'}, status=400)
    
    question = Question.objects.create(
        quiz = quiz,
        question_text = question_text,
        question_type = question_type,
    )

    if question.is_mcq:
        options = data.get('options', [])
        correct_option = data.get('correct_option')

        option_index = 1

        for text in options:
            if text.strip():
                Option.objects.create(question=question, text=text)
                if str(option_index) == str(correct_option):
                    question.correct_answer = text.strip()
            option_index += 1

        question.save()

    elif question.is_fill_in_blank:
        blank_value = data.get('blank_word')
        if blank_value:
            index_str, blank_word = blank_value.split('|')
            index = int(index_str)
            words = list(re.finditer(r"\b[\w']+\b", question_text))
            
            start, end = words[index].span()
            updated_text = question_text[:start] + "_____" + question_text[end:]
            question.question_text = updated_text
            question.correct_answer = blank_word
            question.save()

    return JsonResponse({'success': True, 'question': serialize_question(question)})
