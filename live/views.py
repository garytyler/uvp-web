import logging

from django.shortcuts import redirect, render

from .forms import InteractorSignUpForm
from .models import Feature

# from django.contrib.auth import get_user_model, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.urls import reverse

log = logging.getLogger(__name__)


def index(request):
    """Route guests according to feature and existing session data.

    If session is already in queued, reroute to guest interface. If queued, reroute to join.
    """
    try:
        feature = Feature.objects.get(pk=1)
    except Feature.DoesNotExist as e:
        log.error(e)
        feature = Feature(pk=1)
        feature.save()

    request.session.save()
    if request.session.session_key in feature.guest_queue:
        return redirect("/interact/")
    else:
        return redirect("/home/")


def home(request):
    if request.method == "POST":
        form_post = InteractorSignUpForm(request.POST)
        if form_post.is_valid():
            request.session["display_name"] = form_post.cleaned_data["your_name"]
            return redirect("/interact/")
    else:
        form_get = InteractorSignUpForm()
    return render(request, "live/home.html", {"form": form_get})


def interact(request):
    return render(
        request,
        "live/interact.html",
        context={
            "guest": {
                "display_name": request.session.get("display_name", None),
                "session_key": request.session.session_key,
            }
        },
    )


def supervise(request):
    return render(request, "live/supervise.html")


def guest_exit(request):
    # TODO Add an exit message
    return redirect("/")


# def login(request):
#     if request.method == "POST":
#         if request.session.test_cookie_worked():
#             request.session.delete_test_cookie()
#             return HttpResponse("You're logged in.")
#         else:
#             return HttpResponse("Please enable cookies and try again.")
#     request.session.set_test_cookie()
#     return render(request, "foo/login_form.html")


# def date_and_time():
#     now = datetime.now()
#     return now.strftime("%A, %d %B, %Y at %X")


# def check_id(request, interactor_name):
#     """
#     TODO: This is a terrible id checker. Make a good id checker.
#     """
#     # Filter the id argument to letters only using regular expressions. URL arguments
#     # can contain arbitrary text, so we restrict to safe characters only.
#     match_object = re.match("[a-zA-Z]+", interactor_name)
#     if match_object:
#         clean_interactor_name = match_object.group(0)
#     else:
#         clean_interactor_name = "Friend"
#     return interactor_name == clean_interactor_name


# User = get_user_model()


# @login_required(login_url="/log_in/")
# def user_list(request):
#     """
#     NOTE: This is fine for demonstration purposes, but this should be
#     refactored before we deploy this app to production.
#     Imagine how 100,000 users logging in and out of our app would affect
#     the performance of this code!
#     """
#     users = User.objects.select_related("logged_in_user")
#     for user in users:
#         user.status = "Online" if hasattr(user, "logged_in_user") else "Offline"
#     return render(request, "live/user_list.html", {"users": users})


# def log_in(request):
#     form = AuthenticationForm()
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)

#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect(reverse("live:user_list"))
#         else:
#             print(form.errors)
#     return render(request, "live/log_in.html", {"form": form})


# @login_required(login_url="/log_in/")
# def log_out(request):
#     logout(request)
#     return redirect(reverse("live:log_in"))


# def sign_up(request):
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("live:log_in"))
#         else:
#             print(form.errors)
#     return render(request, "live/sign_up.html", {"form": form})
