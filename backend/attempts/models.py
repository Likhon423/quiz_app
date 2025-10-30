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

    is_submitted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

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