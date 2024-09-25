from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# class Subject(models.Model):
#     subject_id = models.IntegerField(primary_key=True)
#     subject_name = models.CharField(max_length=255)
#     description = models.TextField()
# class Exam(models.Model):
#     exam_id = models.IntegerField(primary_key=True)
#     subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     exam_name = models.CharField(max_length=255)
#     exam_duration = models.IntegerField()
# class Question(models.Model):
#     question_id = models.IntegerField(primary_key=True)
#     subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     question_text = models.TextField()
#     clo_id = models.IntegerField()
# class Answer(models.Model):
    
class Question(models.Model):
    content = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()
    #tim hieu lai ve date_taken : luu thoi gian tu luc bat dau lam bai
    submission_time = models.DateTimeField(default=timezone.now)
    #thêm submission_time để cơ sở dữ liệu biết cần lưu trữ thông tin này
    def __str__(self):
        return f'{self.user.username} - {self.score}'


