from django import forms
from .models import Quiz, Question, Option

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded px-2 py-1',
                'placeholder': 'Quiz title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border rounded px-2 py-1 resize-none',
                'placeholder': 'Description (optional)',
                'rows': 3,
            }),
        }

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