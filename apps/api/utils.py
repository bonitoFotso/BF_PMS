import random
import string
from datetime import datetime
from django.contrib import auth
from rest_framework_simplejwt import tokens
from typing import Any, Tuple
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from apps.authentication.models import User

#User = auth.get_user_model()


def get_tokens_for_user(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }


def get_new_access_token(refresh_token):
    refresh = tokens.RefreshToken(token=refresh_token)
    return str(refresh.access_token)


def get_user_from_token(token):
    token = tokens.RefreshToken(token=token)
    try:
        return User.objects.get(id=token.get("user_id"))
    except User.DoesNotExist:
        return None


def update_model(instance: Any, data_dict: dict) -> Any:
    for key, value in data_dict.items():
        instance.key = value
    return instance


def generate_random_password():
    password_seq = (
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
        + string.punctuation
    )
    password = "".join(random.sample(password_seq, 16))
    return password
