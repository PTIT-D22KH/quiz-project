from django.contrib import admin
from .models import Question, Answer, QuizResult

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizResult)