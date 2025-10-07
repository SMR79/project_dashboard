from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CrispyAuthenticationForm, UserEditForm
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

# create user list view
def get_user_list(request):
    users = CustomUser.objects.all()
    # Apply filters if any
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query)  # Example filter
        
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if the request is AJAX, return only the table part
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'users/user_list_table.html', {'page_obj': page_obj})

    return render(request, 'users/user_list.html', {'page_obj': page_obj})


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Účet byl úspěšně vytvořen, nyní se můžete přihlásit.")
            return redirect("user_list")
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

    # Pokud session neobsahuje previous_url, uložíme odkaz odkud přišel uživatel
    if 'previous_url' not in request.session:
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            request.session['previous_url'] = previous_url

    # get the last message if exists
    all_messages = list(messages.get_messages(request))
    print(all_messages)
    last_message = all_messages[-1] if all_messages else None

    return render(request, 'users/user_detail.html', {
        'detail_user': detail_user,
        'back_url': request.session.get('previous_url', '/'),  # fallback "/"
        'last_message': last_message,
    })

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id) 
    
    if request.method == "POST":
        form = UserEditForm(
            request.POST,
            instance=user,
            current_user=request.user,                     
        )
        if form.is_valid():
            form.save()            
            messages.success(request, "User details updated successfully.")
            return redirect('user_detail', user_id=user.id)        
    else:
        form = UserEditForm(
            instance=user,
            current_user=request.user,        
        )

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

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Nepovolíme smazání sami sebe (optional bezpečnostní pravidlo)
    if user == request.user:
        messages.error(request, "You cannot delete yourself!")
        return redirect('user_detail', user_id=user.id)

    user.delete()
    messages.success(request, f"User {user.username} has been deleted.")

    # Redirect to the previous page if available
    back_url = request.session.get('previous_url', None)
    if back_url:
        return redirect(back_url)

    return redirect('user_list')  # Redirect to user detail page 


def reset_user_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 or not password2:
            messages.error(request, "Both password fields are required.")
            return redirect('user_detail', user_id=user.id)

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('user_detail', user_id=user.id)

        user.password = make_password(password1)
        user.save()
        messages.success(request, f"Password for {user.username} has been changed.")
        return redirect('user_detail', user_id=user.id)

    return redirect('user_detail', user_id=user.id)