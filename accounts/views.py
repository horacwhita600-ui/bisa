from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# REGISTER
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get("email")  # gunakan email sebagai username
            user.set_password(form.cleaned_data.get("password"))  # pastikan password di-hash
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, "Email not registered.")
                return redirect("login")
            user = authenticate(request, username=email, password=password)  # gunakan email sebagai username
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")

# DASHBOARD (setelah login)
@login_required
def dashboard_view(request):
    return render(request, "monitoring/dashboard.html")
