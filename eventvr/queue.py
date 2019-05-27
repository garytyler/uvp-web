from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from eventvr.models import Feature, Guest


def delete_guest_by_session_id(session_id):
    Guest.objects.filter(session_id=session_id).delete()
