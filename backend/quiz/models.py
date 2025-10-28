from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Quiz(models.Model):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes',
        limit_choices_to={'role': 'tutor'}
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'MCQ'),
        ('fill', 'Fill in the blank'),
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    correct_answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.question_text[:50]} ({self.get_question_type_display()})"
    
    @property
    def is_mcq(self):
        return self.question_type == 'mcq'
    
    @property
    def is_fill_in_blank(self):
        return self.question_type == 'fill'


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        limit_choices_to={'question_type': 'mcq'}
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Option for '{self.question.question_text[:30]}': {self.text}"
    
    def clean(self):
        if not self.question.is_mcq:
            raise ValidationError("Options can only be added to MCQ questions.")
