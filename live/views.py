import logging

from django.shortcuts import get_object_or_404, redirect, render

from .forms import GuestSignUpForm
from .models import Feature

log = logging.getLogger(__name__)


def guest_signup(request, feature_slug):
    if request.method == "POST":
        form_post = GuestSignUpForm(request.POST)
        if form_post.is_valid():
            request.session["feature_slug"] = feature_slug
            request.session["guest_name"] = form_post.cleaned_data["guest_name"]
            request.session.save()
            return redirect(f"/{feature_slug}/interact/")
        else:
            return redirect(f"/{feature_slug}/")
    else:
        feature = get_object_or_404(Feature, slug=feature_slug)
        request.session.save()
        if request.session.session_key in feature.guest_queue:
            return redirect(f"/{feature_slug}/interact/")
        else:
            form_get = GuestSignUpForm()
            return render(request, "live/guest_signup.html", {"form": form_get})


def guest_interact(request, feature_slug):
    return render(
        request,
        "live/guest_interact.html",
        context={
            "context_data": {
                "feature_slug": request.session["feature_slug"],
                "guest_name": request.session["guest_name"],
                "session_key": request.session["session_key"],
            }
        },
    )


def supervise(request):
    return render(request, "live/supervise.html")


def guest_exit(request):
    return redirect("/")
