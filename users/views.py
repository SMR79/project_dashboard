from django.shortcuts import render, redirect
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
            return redirect("user_list")  
    else:
        form = CustomUserForm()
    return render(request, "users/register.html", {"form": form})

def login(request):
    pass

def logout(request):
    pass