from eventvr.models import DisplayClient


def run():
    # Fetch all questions
    print(DisplayClient.objects.all())
