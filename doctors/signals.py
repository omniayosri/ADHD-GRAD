from django.db.models.signals import post_save
from django.dispatch import receiver
from oauth2_provider.models import AccessToken, RefreshToken
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        expires = timezone.now() + timedelta(settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
        tok = generate_token()
        app = Application.objects.first()
        access_token = AccessToken.objects.create(user=instance, application=app, expires=expires, token=tok)

        refresh_token = generate_token()
        RefreshToken.objects.create(user=instance, token=refresh_token, application=app, access_token=access_token)




from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'otp': reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for your {title}".format(title="ADHD account"),
        # message:
        email_plaintext_message,
        # from:
        "admin@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()