from django.contrib import admin
from .models import Category,Quiz,Option,Question,QuizResult,StudentAnswer,All_questions

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'question_type', 'CLO', 'quiz_id', 'difficulty')

class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'option_text', 'is_correct')
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category','duration', 'quiz_file', 'created_at', 'updated_at')
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'quiz_result_id', 'answer_text')
class All_questionsAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'CLO', 'difficulty', 'question_type', 'category', 'subtopic')
    list_filter = ('difficulty', 'question_type', 'category')
    search_fields = ('question_text', 'CLO')

    fieldsets = (
        (None, {
            'fields': ('question_text', 'CLO', 'difficulty', 'question_type', 'category', 'subtopic')
        }),
        ('Options', {
            'fields': ('option_1', 'option_2', 'option_3', 'option_4', 'correct_answer'),
            'classes': ('mcq_options',),
        }),
    )

    class Media:
        js = ('admin/js/question_type_toggle.js',)
admin.site.register(All_questions,All_questionsAdmin)
admin.site.register(Category)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Option,OptionAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(QuizResult)
admin.site.register(StudentAnswer,StudentAnswerAdmin)



