import json
import re
from datetime import datetime

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse
from django.utils.safestring import mark_safe

from .forms import InteractorSignUpForm

# import the logging library
# import logging

# Get an instance of a logger
# log = logging.getLogger("django.server")
# log.setLevel(logging.DEBUG)
# print("LOG LEVEL:", log.getEffectiveLevel())
# logging.basicConfig(filename="example.log", filemode="w", level=logging.DEBUG)


def join(request):
    # log.debug("debug test")
    # log.info("info test")
    # log.warning("warning test")
    # log.error("error test")
    # log.critical("critical test")

    if request.method == "POST":
        form_post = InteractorSignUpForm(request.POST)
        if form_post.is_valid():
            request.session["display_name"] = form_post.cleaned_data["your_name"]
            return HttpResponseRedirect("/queue/")
    else:
        form_get = InteractorSignUpForm()
    return render(request, "eventvr/join.html", {"form": form_get})


def queue(request):
    # print(dir(request.session))
    # print(type(request.session.session_key))
    return render(
        request,
        "eventvr/queue.html",
        context={
            "interactor": {
                "display_name": request.session.get("display_name", None),
                "session_key": request.session.session_key,
            },
            "all_sessions": [s.get_decoded() for s in Session.objects.all()],
        },
    )
    # if not interactor_name:
    #     interactor_name = request.session.get("interactor_name", None)
    # request.session["interactor_name"] = interactor_name

    # all_sessions = [s.get_decoded() for s in Session.objects.all()]

    # return render(
    #     request,
    #     "eventvr/queue.html",
    #     context={
    #         "interactor_name": mark_safe(json.dumps(request.session["interactor_name"])),
    #         "all_sessions": all_sessions,
    #     },
    # )


def interact(request):
    return render(
        request,
        "eventvr/interact.html",
        # context={"interactor_name_json": mark_safe(json.dumps(interactor_name))},
        # context={"interactor_name": interactor_name},
    )


def login(request):
    if request.method == "POST":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, "foo/login_form.html")


def date_and_time():
    now = datetime.now()
    return now.strftime("%A, %d %B, %Y at %X")


def check_id(request, interactor_name):
    """
    TODO: This is a terrible id checker. Make a good id checker.
    """
    # Filter the id argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", interactor_name)
    if match_object:
        clean_interactor_name = match_object.group(0)
    else:
        clean_interactor_name = "Friend"
    return interactor_name == clean_interactor_name


User = get_user_model()


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
