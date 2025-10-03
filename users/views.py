from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CrispyAuthenticationForm, UserEditForm

# create user list view
def get_user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Účet byl úspěšně vytvořen, nyní se můžete přihlásit.")
            return redirect("login")
    else:
        form = CustomUserForm()
    return render(request, "users/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = CrispyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('welocome')
    else:
        form = CrispyAuthenticationForm()
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


def get_user_detail(request, user_id):
    detail_user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/user_detail.html', {'detail_user': detail_user})

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserEditForm(instance=user, current_user=request.user)
    return render(request, 'users/edit_user.html', {'form': form, 'edit_user': user})

def generate_user_report(request):
    users = CustomUser.objects.all()
    stats = {
        "admin": CustomUser.objects.filter(role="admin").count(),
        "supervisor": CustomUser.objects.filter(role="supervisor").count(),
        "staff": CustomUser.objects.filter(role="staff").count(),   
        "total": users.count(),
    }
    return render(request, 'users/user_report.html', {'stats': stats})