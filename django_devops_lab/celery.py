from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_devops_lab.settings')

celery_worker = Celery('django_devops_lab')

celery_worker.config_from_object('django.conf:settings', namespace='CELERY')

celery_worker.autodiscover_tasks()