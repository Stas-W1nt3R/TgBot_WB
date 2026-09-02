from celery import shared_task
from celery.schedules import crontab
from TgBot_WB.celery import app

from .models import UserTracking

@shared_task
def check_all_price():
    trackings = UserTracking.objects.filter(is_active=True)

    for tracking in trackings:
        cryptocurrency_price = tracking.cryptocurrency.price
        check_price.delay(tracking.target_price, cryptocurrency_price)

@shared_task
def check_price(target_price,cryptocurrency_price):
    if target_price < cryptocurrency_price:
        return False
    else:
        return True


app.conf.beat_schedule = {
    'check-price': {
        'task': 'tasks.check_all_price',
        'schedule': crontab(minute='*/10'),
    }
}