from celery import shared_task
import time
# this task runs once a day
# run it again 5 minutes later if it didn't finish (conditionally re-run)
# or time.sleep


@shared_task
def add(x, y):
    return (x + y)
