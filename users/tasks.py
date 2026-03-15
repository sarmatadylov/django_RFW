from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
import random



@shared_task
def add(x, y):
    sleep(10)
    print(x + y)
    return  "OK"


@shared_task
def send_otp_email(email, code):
    print(10 * "#")
    send_mail(
        "Привет ДП",
        f"вот твой одноразовый код {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "SENT"


@shared_task
def todo_homework():
    print(10 * "$")
    send_mail(
        "Привет друг",
        "Пора делать домашку",
        settings.EMAIL_HOST_USER,
        [""],
        fail_silently=False,
    )
    return "BOLDU"


#можно запускать через delay()
@shared_task
def save_random_number():
    number = random.randint(1, 100)
    print(f"Сгенерированное число: {number}")
    return number


#можно запускать по расписанию (crontab)
@shared_task
def clear_temp_data():
    print("Очистка временных данных...")
    sleep(5)
    print("Очистка завершена")
    return "CLEARED"


#еще одна задача с SMTP
@shared_task
def send_daily_email():
    send_mail(
        "Ежедневное напоминание",
        "Не забудь проверить свои задачи сегодня",
        settings.EMAIL_HOST_USER,
        ["тут_email"],
        fail_silently=False,
    )
    return "EMAIL SENT"