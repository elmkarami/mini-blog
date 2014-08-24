from datetime import datetime, timedelta

from celery import task

from apps.blog.models import Tweet


@task()
def hashtag_task():
    """
    A periodic task for deleting all old messages over 10 days.
    """
    date = datetime.now() - timedelta(10)
    Tweet.objects.filter(created__lt=date).delete()    
