from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "celery_project.settings"
)  # project name

app = Celery("celery_project")  # project name in celery instance

"""
for changing timezone:
app.conf.enabled_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
"""

app.config_from_object(settings, namespace="CELERY")

# celery beats settings
app.conf.beat_schedule = {}
# Load task modules from all registered Django app configs.

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request}")  # print(f"Request: {self.request!r}")
