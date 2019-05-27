from django.apps import AppConfig
from django.db.utils import DatabaseError


class EventVRConfig(AppConfig):
    name = "eventvr"
    ready_has_run = False

    def ready(self):
        if self.ready_has_run:
            return

        # # Do your stuff here, and then set the flag
        # from django.contrib.sessions.models import Session

        # try:
        #     Session.objects.all().delete()
        # except DatabaseError as e:
        #     print(e)

        # for s in Session.objects.all():
        #     s.delete()
        #     s.save()

        self.ready_has_run = True
