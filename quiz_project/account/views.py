from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile
from django.views.decorators.cache import never_cache
from django.templatetags.static import static
from quiz.models import Quiz, Category, Question, Option, QuizResult, StudentAnswer
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser

# Create your views here.
@never_cache
# def register(request):
#     # if request.user.is_authenticated:
#     #     return redirect('profile', request.user.username)

#     if request.method == 'POST':
#         email=request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             # check if email is not same
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, "Email Already Used. Try to Login.")
#                 return redirect('register')
#             # check if username is not same
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, "Username Already Taken.")
#                 return redirect('register')
#             else:
#                 # create user
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()

#                 # log in the user and redirect to profile
#                 user_login = auth.authenticate(username=username, password=password)
#                 auth.login(request, user_login)


#                 # create profile for new user
#                 user_model = User.objects.get(username=username)
#                 new_profile = Profile.objects.create(user=user_model,email=email)
#                 new_profile.save()
#                 return redirect('login')
#         else:
#             messages.info(request, 'password not matched')
#             return redirect('register',username)

#     context = {}
#     return render(request, "register1.html", context)
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        studen_id = request.POST['studen_id']
        user_class = request.POST['user_class']
        

        if password == password2:
            # check if email is not same
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used. Try to Login.")
                return redirect('register')
            # check if username is not same
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken.")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, email=email, gender=gender, studen_id=studen_id, user_class=user_class)
                new_profile.save()
                return redirect('registerOk')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

    context = {}
    return render(request, "register1.html", context)

@login_required(login_url='login')
@never_cache
def profile(request, username):
    if request.user.username != username:
        return HttpResponseForbidden("You are not allowed to view this profile.")

    user_object=User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    default_img_url = static('')
    # profile user
    context={
        "user_profile":user_profile,
        'default_img_url': default_img_url,
    }
    return render(request, "profile.html",context)
@never_cache
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('profile', request.user.username)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, 'Credentials Invalid!')
            return redirect('login')

    return render(request, "login.html")


@login_required
def editProfile(request):

    user_object = request.user
    user_profile = request.user.profile

    if request.method == "POST":
        # Image
        if request.FILES.get('profile_img') != None:
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()

        # Email
        if request.POST.get('email') != None:
            u = get_object_or_404(User, email=request.POST.get('email'))

            if u == None:
                user_object.email = request.POST.get('email')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Email Already Used, Choose a different one!")
                    return redirect('edit_profile')

        # Username
        if request.POST.get('username') != None:
            u = get_object_or_404(User, username=request.POST.get('username'))

            if u == None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Username Already Taken, Choose an unique one!")
                    return redirect('edit_profile')

        # firstname lastname
        user_object.first_name = request.POST.get('firstname')
        user_object.last_name = request.POST.get('lastname')
        user_object.save()

        # gender, studen_id, user_class
        user_profile.gender = request.POST.get('gender')
        user_profile.studen_id = request.POST.get('studen_id')
        user_profile.user_class = request.POST.get('user_class')
        user_profile.save()

        return redirect('profile', user_object.username)


    context = {"user_profile": user_profile}
    return render(request, 'profile-edit.html', context)

@login_required(login_url='login')
@never_cache
def logout(request):
    auth.logout(request)
    return redirect('home')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
def registerOk(request):
    return render(request, 'registerOk.html')