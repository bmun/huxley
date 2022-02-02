import os
import django

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huxley.settings')

django.setup()

# import the tasks once django is setup
# from huxley.core.tasks import poll_waiver

app = Celery('huxley')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, poll_waiver.s(), name='polling for waivers')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
