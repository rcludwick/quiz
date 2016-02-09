from django.contrib import admin
from .models import Quiz, UserQuiz, Question


# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Quiz.questions.through


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ('question', 'answer')
    fields = ('question', 'answer')


@admin.register(Quiz)
class Quiz(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (QuestionInline,)
    exclude = ('questions',)


@admin.register(UserQuiz)
class UserQuiz(admin.ModelAdmin):
    list_display = ('name', 'num_correct', 'quiz')
