from django.conf import settings
from django.core.mail import send_mail


def send_email(subject: str, message: str, emails: list[str]):
    send_mail(subject, message, settings.EMAIL_HOST_USER, emails, html_message=message, fail_silently=False)
