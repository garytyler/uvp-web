import logging

from django.shortcuts import get_object_or_404, redirect, render

from .forms import InteractorSignUpForm
from .models import Feature

log = logging.getLogger(__name__)


def guest_welcome(request, feature_slug):
    if request.method == "POST":
        form_post = InteractorSignUpForm(request.POST)
        if form_post.is_valid():
            request.session["feature_slug"] = feature_slug
            request.session["display_name"] = form_post.cleaned_data["your_name"]
            request.session.save()
            return redirect("/guest/interact/")
    else:
        feature = get_object_or_404(Feature, slug=feature_slug)
        if request.session.session_key in feature.current_guests:
            return redirect("/guest/interact/")
        else:
            form_get = InteractorSignUpForm()
            return render(request, "live/welcome.html", {"form": form_get})


def guest_interact(request):
    return render(
        request,
        "live/interact.html",
        context={
            "guest": {
                "feature_slug": request.session["feature_slug"],
                "display_name": request.session["display_name"],
                "session_key": request.session.session_key,
            }
        },
    )


def supervise(request):
    return render(request, "live/supervise.html")


def guest_exit(request):
    return redirect("/")
