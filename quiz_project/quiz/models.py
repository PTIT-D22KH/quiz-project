from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
# import random
# import string

# def generate_random_id():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    quiz_file = models.FileField(upload_to='quiz/' , null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(default=45)
    total_questions = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title
    
    

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blank'),
    ]
    #  add category as foreign key
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    # add subtopic
    subtopic = models.CharField(max_length=255,null=True, blank=True)
    id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    CLO = models.IntegerField(default=1)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    difficulty = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.question_text}'

class Option(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text}"

class QuizResult(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user_id.username} - {self.quiz_id.title}- {self.score}"

# class StudentAnswer(models.Model):
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     quiz_result_id = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
#     answer_text = models.TextField()
#     def __str__(self):
#         return f'{self.question_id.question_text} - {self.answer_text}'

class StudentAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_result_id = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.FloatField(default=0)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studen_id = models.CharField(max_length=15, blank=True, null=True)
    is_mark = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.question_id.question_text} - {self.answer_text}'

class All_questions(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blank'),
    ]

    question_text = models.CharField(max_length=255)
    CLO = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    subtopic = models.CharField(max_length=255)

    # Fields for MCQ
    option_1 = models.CharField(max_length=255, blank=True, null=True)
    option_2 = models.CharField(max_length=255, blank=True, null=True)
    option_3 = models.CharField(max_length=255, blank=True, null=True)
    option_4 = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        if self.question_type == 'MCQ':
            if not all([self.option_1, self.option_2, self.correct_answer]):
                raise ValidationError("MCQ questions must have at least two options and a correct answer.")
        elif self.question_type == 'FIB':
            if self.option_1 or self.option_2 or self.option_3 or self.option_4 or self.correct_answer:
                raise ValidationError("FIB questions should not have options or a correct answer.")

    def __str__(self):
        return f'{self.question_text} - {self.CLO} - {self.difficulty} - {self.question_type}'



