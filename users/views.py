from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserForm
from .models import CustomUser

# create user list view
def get_user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  
    else:
        form = CustomUserForm()
    return render(request, "users/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('welocome')  # po přihlášení přesměrujeme na projekty
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})
    

# view to handle user logout
def logout_user(request):
    logout(request)
    return redirect("login")


def welcome(request):
    if request.user.is_authenticated:
        user = request.user
        name = user.first_name or user.username
    else:
        name = "Guest"
    return render(request, "users/welcome.html", {"name": name})
    