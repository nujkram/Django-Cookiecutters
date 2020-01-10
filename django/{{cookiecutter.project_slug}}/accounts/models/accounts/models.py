"""
{{ cookiecutter.project_name }} {{ cookiecutter.version }}
{{ cookiecutter.description }}

Account model

---
{{ cookiecutter.author_name}}
{{ cookiecutter.email}}
"""
import logging
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.apps import apps

from .constants import USERNAME_REGEX, USER_TYPE_CHOICES, USER, ADMIN, SUPERADMIN
from .managers import AccountManager

logger = logging.getLogger(__name__)


class Account(AbstractBaseUser):
    """
    Base Account model
    Fields:
        - created: DateTimeField
        - updated: DateTimeField
        - uuid: UUIDField
        - username: CharField
        - email: EmailField
        - is_active: BooleanField
        - is_admin: BooleanField
        - user_type: CharField
        - user_settings: JSONField
    """
    # Fields
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username can only contain alphanumeric characters and the following characters: . -',
                code='Invalid Username'
            )
        ],
        unique=True,

    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default=USER, max_length=6)

    # NonRelational data
    user_settings = JSONField(default=dict)
    created_by = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        related_name="account_creator",
        db_index=False
    )

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        ordering = ('username', '-created',)

    ################################################################################
    # Model methods
    ################################################################################


@receiver(post_save, sender=Account)
def scaffold_account(sender, instance=None, created=False, **kwargs):
    if created:
        Profile = apps.get_model('profiles.Profile')
        Token.objects.create(user=instance)
        try:
            profile = Profile.objects.create(
                account=instance
            )
            logger.info(f"{profile} created for {instance}")
        except IntegrityError as e:
            logger.error(f"IntegriyError: {e} for {instance}")
            pass