import logging
from celery import shared_task
from django.core.mail import send_mail
from .models import Post
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from user.models import User
from parser.scrap_news_from_limonKg import ScrapNewsLimonKG

@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={
        'max_retries': 5,
        'countdown': 30,
    }
)
def send_message():
    today = datetime.now().date()
    posts = Post.objects.filter(added_at__date = today)
    users = User.objects.all()

    if not posts.exists():
        logging.info("Нет постов для рассылки.")
        return

    if not users.exists():
        logging.info("Нет пользователей для рассылки.")
        return
    
    for user in users:
        context = {
            'posts': posts,
            'user_name': user.name or user.email,
            'site_url': 'http://127.0.0.1:8000/post'
        }
        html_message = render_to_string('send_message.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject='Сервис новостей!',
                message=plain_message,
                from_email='NewsService@gmail.com',
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            logging.error(f"Ошибка при отправке письма {user.email}: {e}")


        logging.info(f"Отправили письмо пользователю {user.email}")

@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={
        'max_retries': 5,
        'countdown': 30,
    }
)
def start_scraper():
    start = ScrapNewsLimonKG()
    starting = start.start()