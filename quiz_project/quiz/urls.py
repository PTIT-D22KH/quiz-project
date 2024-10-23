from django.urls import path
from . import views

urlpatterns = [
    path('all_quiz/', views.all_quiz_view, name='all_quiz'),
    path('search/<str:category>', views.search_view, name='search'),
    path('start_quiz/<int:quiz_id>/', views.quiz_view, name='start_quiz'),
    # path('quiz_result/<int:quiz_id>/', views.quiz_result_view, name='quiz_result'),
    path('quiz_result/<int:quiz_id>/<int:quiz_result_id>', views.quiz_result_view, name='quiz_result'),
    path('addquiz', views.addQuiz, name='addquiz'),
    path('mark_quiz/<int:quiz_id>', views.mark_quiz, name='mark_quiz'),
    path('quiz_leaderboard/<int:quiz_id>', views.quiz_leaderboard_view, name='quiz_leaderboard'),
    path('createquizfromdb', views.create_quiz_from_db, name='createQuizFromDB'),
]
