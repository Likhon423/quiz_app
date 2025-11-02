from django.db import models
from django.conf import settings
from quiz.models import Quiz, Question

# Create your models here.
class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
    )

    current_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='current'
    )

    is_submitted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def calculate_score(self):
        correct = 0
        for answer in self.answers.select_related('question'):
            if answer.selected_answer and answer.selected_answer.strip().lower() == answer.question.correct_answer.strip().lower():
                correct += 1
        self.score = correct
        self.is_submitted = True
        self.save(update_fields=['score', 'is_submitted'])

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
    

class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    selected_answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Answer for {self.question} by {self.attempt.student.username}"