from django import forms
from .models import Quiz, Question, Option

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'correct_answer']
        widgets = {
            'question_text': forms.Textarea(),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']