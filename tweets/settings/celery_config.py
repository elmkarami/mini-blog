from celery.schedules import crontab

import djcelery


djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_DISABLE_RATE_LIMITS = False


CELERYBEAT_SCHEDULE = {
    'delete-every-day': {
        'task': 'apps.blog.tasks.hashtag_task',
        'schedule': crontab(minute=0, hour=0) # Every day at midnight
    },
}
