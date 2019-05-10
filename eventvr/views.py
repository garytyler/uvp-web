import re
import json
from datetime import datetime
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.middleware.csrf import CsrfViewMiddleware


def date_and_time():
    now = datetime.now()
    return now.strftime("%A, %d %B, %Y at %X")


def check_id(request, visitorid):
    """
    TODO: This is a terrible id checker. Make a good id checker.
    """
    # Filter the id argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", visitorid)
    if match_object:
        clean_visitorid = match_object.group(0)
    else:
        clean_visitorid = "Friend"
    return visitorid == clean_visitorid


User = get_user_model()


def index(request):
    return render(request, "eventvr/index.html", {})


def queue(request, visitorid):
    return render(
        request,
        "eventvr/queue.html",
        {"visitorid_json": mark_safe(json.dumps(visitorid))},
    )
    # return CsrfViewMiddleware.process_view(
    #     callback=request,
    #     # "eventvr/queue.html",
    #     callback_args=[],
    #     callback_kwargs={"visitorid_json": mark_safe(json.dumps(visitorid))},
    # )


@login_required(login_url="/log_in/")
def user_list(request):
    """
    NOTE: This is fine for demonstration purposes, but this should be
    refactored before we deploy this app to production.
    Imagine how 100,000 users logging in and out of our app would affect
    the performance of this code!
    """
    users = User.objects.select_related("logged_in_user")
    for user in users:
        user.status = "Online" if hasattr(user, "logged_in_user") else "Offline"
    return render(request, "eventvr/user_list.html", {"users": users})


def log_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse("eventvr:user_list"))
        else:
            print(form.errors)
    return render(request, "eventvr/log_in.html", {"form": form})


@login_required(login_url="/log_in/")
def log_out(request):
    logout(request)
    return redirect(reverse("eventvr:log_in"))


def sign_up(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("eventvr:log_in"))
        else:
            print(form.errors)
    return render(request, "eventvr/sign_up.html", {"form": form})
