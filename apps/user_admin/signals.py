from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.utils import timezone
import json

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

@receiver(post_migrate)
def create_periodic_tasks(sender, **kwargs):
    schedule = CrontabSchedule.objects.filter(
        minute='*',
        hour='*',
        day_of_month='*',
        month_of_year='*',
        day_of_week='*'
    )
    if schedule.count() > 1:
        first_schedule = schedule.first()
        for schedule in schedule[1:]:
            schedule.delete()
        print(f"duplicate schedules, kept ID: {first_schedule.id}")

    schedule = CrontabSchedule.objects.get_or_create(
        minute='*',
        hour='*',
        day_of_month='*',
        month_of_year='*',
        day_of_week='*'
    )
    schedule = schedule[0]

    if not PeriodicTask.objects.filter(name="Task-Sincroniza-LGPD-Aceitos").exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name="Task-Sincroniza-LGPD-Aceitos",
            task="Task-Sincroniza-LGPD-Aceitos",  
            args=json.dumps([]),  
            kwargs=json.dumps({}),  
            enabled=True,
            start_time=timezone.now(),  
        )
