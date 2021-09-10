import os
import django

from celery import Celery
from huxley.core.tasks import add

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huxley.settings.main')

django.setup()

app = Celery('huxley')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, add.s(6, 7), name='add every 10')


@app.task
def hello(s):
    return s


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
