from django.contrib import admin
from .models import Quiz, Question, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ('text',)
    show_change_link = True


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('question_text', 'question_type', 'correct_answer')
    show_change_link = True


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'created_at')
    search_fields = ('title', 'tutor__username')
    list_filter = ('created_at',)
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type')
    list_filter = ('question_type', 'quiz')
    search_fields = ('question_text', 'quiz__title')
    inlines = [OptionInline]


class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    search_fields = ('text', 'question__question_text')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
