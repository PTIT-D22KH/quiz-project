from django.shortcuts import render, redirect
from .models import Question, Answer, QuizResult
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def quiz_view(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        score = 0
        correct_answers = 0
        incorrect_answers = 0
        for question in questions:
            selected_answer = request.POST.get(str(question.id))
            if selected_answer == question.correct_answer:
                score += 1
                correct_answers += 1
            else:
                incorrect_answers += 1
        
        # Lưu kết quả vào cơ sở dữ liệu
        QuizResult.objects.create(
            user=request.user,
            score=score * 10 / questions.count(),
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            submission_time = timezone.now()
            #cần cập nhật view khi người dùng nộp bài, thời gian nộp bài sẽ được lưu vào cơ sở dữ liệu
        )
        
        return render(request, 'quiz/result.html', {
            'score': score * 10 / questions.count(),
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers
        })
    return render(request, 'quiz/quiz.html', {'questions': questions})