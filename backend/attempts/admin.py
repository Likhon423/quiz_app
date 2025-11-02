from django.contrib import admin
from .models import QuizAttempt, AttemptAnswer
from quiz.models import Question


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer', 'correct_answer_display')
    can_delete = False

    def correct_answer_display(self, obj):
        return obj.question.correct_answer if obj.question else "-"
    correct_answer_display.short_description = "Correct Answer"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'quiz', 'current_question', 'score', 'is_submitted')
    list_filter = ('is_submitted', 'quiz')
    search_fields = ('student__username', 'quiz__title')
    readonly_fields = ('score',)
    ordering = ('-id',)
    inlines = [AttemptAnswerInline]

    fieldsets = (
        ('Student & Quiz Info', {
            'fields': ('student', 'quiz', 'current_question')
        }),
        ('Progress', {
            'fields': ('is_submitted', 'score')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "current_question":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                attempt = QuizAttempt.objects.filter(pk=obj_id).select_related("quiz").first()
                if attempt and attempt.quiz:
                    field.queryset = Question.objects.filter(quiz=attempt.quiz)
                else:
                    field.queryset = Question.objects.none()
            else:
                field.queryset = Question.objects.none()
        return field


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt', 'question', 'selected_answer', 'correct_answer_display')
    list_filter = ('attempt__quiz',)
    search_fields = (
        'attempt__student__username',
        'question__question_text',
        'selected_answer'
    )
    ordering = ('id',)

    def correct_answer_display(self, obj):
        return obj.question.correct_answer if obj.question else "-"
    correct_answer_display.short_description = "Correct Answer"
