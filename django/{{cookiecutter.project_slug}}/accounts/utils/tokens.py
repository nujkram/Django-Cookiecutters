from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token

# this return left time
from accounts.controllers.restapi.account.serializers import AccountPrivateSerializer
from accounts.models import Account


def expires_in(token) -> timedelta:
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_LIFETIME) - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


def user_auth_data(user: Account) -> Dict:
    token = user.auth_token

    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = AccountPrivateSerializer(user)

    return {
        'user': user_serialized.data,
        'expires_in': expires_in(token).seconds,
        'token': token.key
    }
