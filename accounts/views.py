from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
import logging

logger = logging.getLogger(__name__)

# REGISTER
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, "Account created successfully. Please log in.")
                logger.info("New user created: %s", user.email)
                return redirect("accounts:login")
            except Exception as e:
                logger.exception("Error creating user")
                messages.error(request, f"Registration failed unexpectedly: {e}")
        else:
            # collect form errors and show them to the user so failures are visible
            errors = []
            for field, field_errors in form.errors.items():
                for err in field_errors:
                    errors.append(f"{field}: {err}")
            messages.error(request, "Registration failed: " + "; ".join(errors))
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            email = email.strip().lower() if email else email
            password = form.cleaned_data.get("password")
            logger.info("Login attempt for email: %s", email)
            # First try authenticating directly using the email as username (we store email->username on register)
            user = authenticate(request, username=email, password=password)
            logger.info("Authenticate(email-as-username) returned: %s for email=%s", user, email)
            username = None
            if user is None:
                # fallback: lookup by email and try authenticate with stored username
                try:
                    found = User.objects.get(email__iexact=email)
                    username = found.username
                    logger.info("Found user for email %s -> username=%s", email, username)
                except User.DoesNotExist:
                    # try matching username case-insensitively (maybe email was stored in username field)
                    found_by_username = User.objects.filter(username__iexact=email).first()
                    if found_by_username:
                        username = found_by_username.username
                        logger.info("Found user by username match: %s", username)
                    else:
                        logger.warning("Login failed: no user with email or username matching %s", email)
                        # Dump some nearby emails for debug (info level)
                        sample = list(User.objects.values_list('email', flat=True)[:10])
                        logger.info("Sample emails in DB: %s", sample)
                        messages.error(request, "Email not registered.")
                        return redirect("accounts:login")
                # if we have a username from the DB (either email->username or username match), try auth
                user = authenticate(request, username=username, password=password)
                logger.info("Authenticate(stored-username) returned: %s for username=%s", user, username)
            if user is not None:
                login(request, user)
                return redirect("monitoring:dashboard")
            else:
                logger.warning("Authentication failed for username %s (email=%s)", username, email)
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

# DASHBOARD (setelah login)
@login_required
def dashboard_view(request):
    return render(request, "monitoring/dashboard.html")
