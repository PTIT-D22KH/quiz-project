from django.urls import path
from . import views
handler404 = 'account.views.custom_404'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit_profile/', views.editProfile, name='edit_profile'),
    path('',views.registerOk,name='registerOk'),
]


