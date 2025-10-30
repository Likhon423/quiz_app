import json, re

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Quiz, Question, Option


def serialize_question(question):
    return {
        'id': question.id,
        'question_text': question.question_text,
        'question_type': question.question_type,
        'correct_answer': question.correct_answer,
        'options': list(question.options.values_list('text', flat=True)) if question.is_mcq else [],
        'blank_word': question.correct_answer if question.is_fill_in_blank else '',
    }

def save_or_update_question(quiz, data, questionObj=None):
    question_text = data.get("question_text").strip()
    question_type = data.get("question_type").strip()

    if not question_text or not question_type:
        return JsonResponse({"success": False, "error": "Invalid data"})
    
    if questionObj:
        question = questionObj
    else:
        question = Question.objects.create(
            quiz = quiz,
            question_text = question_text,
            question_type = question_type,
        )
    
    question.question_text = question_text
    question.question_type = question_type

    if question.is_mcq:
        options = data.get('options', [])
        correct_option = data.get('correct_option')

        question.options.all().delete()

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

    return {'success': True, 'question': serialize_question(question)}



@login_required
def get_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    questions = quiz.questions.all()
    data = [serialize_question(q) for q in questions]
    return JsonResponse({'questions': data})


@login_required
@require_http_methods(["POST"])
def save_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    data = json.loads(request.body.decode('utf-8'))

    result = save_or_update_question(quiz, data)
    return JsonResponse(result, status=200 if result['success'] else 400)


@login_required
@require_http_methods(["PUT"])
def update_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)

    data = json.loads(request.body)
    result = save_or_update_question(quiz, data, question)
    return JsonResponse(result, status=200 if result['success'] else 400)


@login_required
@require_http_methods(["DELETE"])
def delete_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    question.delete()
    return JsonResponse({"success": True})

@login_required
@require_http_methods(["DELETE"])
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, tutor=request.user)
    quiz.delete()
    return JsonResponse({"success": True})