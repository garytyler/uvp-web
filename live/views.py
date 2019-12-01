import logging

from django.shortcuts import redirect, render

from .forms import InteractorSignUpForm
from .models import Feature

log = logging.getLogger(__name__)


def index(request):
    """Route guests according to feature and existing session data.

    If session is already in queued, reroute to guest interface. If queued, reroute to join.
    """
    # request.user.save()
    # print(len(request.session["session_key"]))
    # print(len(request.session.session_key))
    # print(request.user.save())

    feature = Feature.objects.get(pk=1)

    # backends.base.SessionBase
    # See: https://docs.djangoproject.com/en/2.2/topics/http/sessions/#using-sessions-in-views

    if request.session.session_key in feature.current_guests:
        return redirect("/interact/")
    else:
        return redirect("/home/")


def home(request):
    if request.method == "POST":
        form_post = InteractorSignUpForm(request.POST)
        if form_post.is_valid():
            request.session["display_name"] = form_post.cleaned_data["your_name"]
            request.session.save()
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
    return redirect("/")
