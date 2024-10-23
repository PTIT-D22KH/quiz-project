from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category, Question, Option, QuizResult, StudentAnswer, All_questions
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.db.models import Max
from django.db.models import OuterRef, Subquery
# from quiz.models import QuizSubmission
from django.contrib import messages

def is_admin(user):
    return user.is_superuser

@login_required(login_url='login')
def all_quiz_view(request):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)

@login_required(login_url='login')
def search_view(request, category):

    # search by search bar
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('-created_at')
    
    # search by category
    elif category != " ":
        quizzes = Quiz.objects.filter(category__name=category).order_by('-created_at')
    
    else:
        quizzes = Quiz.objects.order_by('-created_at')


    categories = Category.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)








@login_required(login_url='login')
@never_cache
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz_id=quiz_id)
    options = Option.objects.filter(question_id__in=questions)

    if not questions.exists():
        # Handle the case where there are no questions in the quiz
        return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions, 'options': options, 'quiz_result': None, 'error': 'No questions available for this quiz.'})

    quiz_result = QuizResult.objects.create(
        user_id=request.user,
        score=0,
        correct_answers=0,
        incorrect_answers=0,
        # quiz_id=questions[0].quiz_id,
        quiz_id=quiz,
        start_time=timezone.now()
    )
    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions, 'options': options, 'quiz_result': quiz_result})

@login_required(login_url='login')
@never_cache
def quiz_result_view(request, quiz_id, quiz_result_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz_id=quiz_id)
    options = Option.objects.filter(question_id__in=questions)
    if request.method == 'POST':
        score = 0
        correct_answers = 0
        incorrect_answers = 0
        heso = 10 / len(questions)
        quiz_result = QuizResult.objects.create(
            user_id=request.user,
            score=0,
            correct_answers=0,
            incorrect_answers=0,
            quiz_id=quiz
        )
        for question in questions:
            if question.question_type == 'MCQ':
                selected_option_id = request.POST.get(str(question.id))
                if selected_option_id:
                    selected_option = Option.objects.get(id=int(selected_option_id))
                    if selected_option.is_correct:
                        score += heso
                        correct_answers += 1
                    else:
                        incorrect_answers += 1
            elif question.question_type == 'FIB':
                answer_text = request.POST.get(str(question.id))
                if answer_text:
                    StudentAnswer.objects.create(
                        question_id=question,
                        quiz_result_id=quiz_result,
                        answer_text=answer_text,
                        studen_id = request.user.profile.studen_id,
                        quiz_id = quiz
                    )
        quiz_result.score = score
        quiz_result.correct_answers = correct_answers
        quiz_result.incorrect_answers = incorrect_answers
        quiz_result.end_time = timezone.now()
        quiz_result.save()

        # Chuyển hướng về trang kết quả hoặc trang khác
        # return redirect('welcome')

    return render(request, 'quiz_result.html', {
        'score': score, 
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'username': request.user.username,
        'total_questions': len(questions)
    })

@login_required(login_url='login')
@user_passes_test(is_admin)
def addQuiz(request):
    return render(request, 'addQuiz.html')
@login_required(login_url='login')
def quiz_leaderboard_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    subquery = QuizResult.objects.filter(
    user_id=OuterRef('user_id'),  
    quiz_id=OuterRef('quiz_id')   
    ).order_by('-score').values('score')[:1]
    results = QuizResult.objects.filter(score = Subquery(subquery), quiz_id = quiz_id).order_by('-score')   
    print(results)
    return render(request, 
                  'quiz_leaderboard.html', 
                  { 'quiz': quiz,
                    'results': results})
@login_required(login_url='login')
@user_passes_test(is_admin)
def create_quiz_from_db(request):
    categories = Category.objects.all()
    questions = All_questions.objects.all()

    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        quiz_description = request.POST.get('quiz_description')
        quiz_category = request.POST.get('quiz_category')
        selected_questions = request.POST.getlist('questions')

        # Create and save the quiz
        quiz = Quiz.objects.create(
            title=quiz_title,
            description=quiz_description,
            category_id=quiz_category,
            total_questions=len(selected_questions)
        )

                # Create new Question objects for the quiz based on selected All_questions
        for q_id in selected_questions:
            all_q = All_questions.objects.get(id=q_id)
            new_question = Question.objects.create(
                quiz_id=quiz,
                question_text=all_q.question_text,
                CLO=all_q.CLO,
                difficulty=all_q.difficulty,
                question_type=all_q.question_type,
                subtopic=all_q.subtopic
            )
            

            
            # Create Option objects for MCQ questions
            if all_q.question_type == 'MCQ':
                options = [all_q.option_1, all_q.option_2, all_q.option_3, all_q.option_4]
                for i, option_text in enumerate(options, start=1):
                    if option_text:
                        Option.objects.create(
                            question_id=new_question,
                            option_text=option_text,
                            is_correct=(option_text == all_q.correct_answer)
                        )
            
            # elif all_q.question_type == 'FIB':
            #     # For Fill in the Blank, we store the correct answer as an option
            #     Option.objects.create(
            #         question=new_question,
            #         # option_text=all_q.correct_answer,
            #         # is_correct=True
            #     )

        messages.success(request, 'Quiz created successfully!')
        return redirect('all_quiz')
        

    # Apply filters
    if 'category' in request.GET:
        categories_filter = request.GET['category'].split(',')
        questions = questions.filter(quiz_id__category_id__in=categories_filter)
    if 'clo' in request.GET:
        clos_filter = request.GET['clo'].split(',')
        questions = questions.filter(CLO__in=clos_filter)
    if 'difficulty' in request.GET:
        difficulties_filter = request.GET['difficulty'].split(',')
        questions = questions.filter(difficulty__in=difficulties_filter)
    if 'type' in request.GET:
        types_filter = request.GET['type'].split(',')
        questions = questions.filter(question_type__in=types_filter)

    # Get distinct CLO values
    clos = questions.values_list('CLO', flat=True).distinct()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions_data = list(questions.values('id', 'question_text', 'CLO', 'difficulty', 'question_type'))
        return JsonResponse({'questions': questions_data})

    context = {
        'categories': categories,
        'clos': clos,
        'questions': questions
    }
    return render(request, 'createQuizFromDB.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def mark_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz_id = quiz_id)
    text_questions = Question.objects.filter(quiz_id=quiz_id, question_type='FIB')
    text_answers = StudentAnswer.objects.filter(question_id__in=text_questions, is_mark=False)
    heso = 10/len(questions)
    if request.method == 'POST':
        for answer in text_answers:
            is_correct = request.POST.get(f'correct_{answer.id}')
            if is_correct:
                answer.score += heso
            if is_correct != None:
                answer.is_mark = True
            answer.save()
        for quiz_result in QuizResult.objects.filter(quiz_id=quiz_id):
            text_score = sum([answer.score for answer in text_answers if answer.quiz_result_id == quiz_result])
            quiz_result.score += text_score
            quiz_result.save()
        return redirect('all_quiz')
    return render(request, 'mark_quiz.html', {'quiz': quiz, 'text_answers': text_answers, 'text_questions': text_questions})