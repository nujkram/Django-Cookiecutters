"""
{{ cookiecutter.project_name }}
{{ cookiecutter.app_name }} {{ cookiecutter.version }}
{{ cookiecutter.module_name }} models
{{ cookiecutter.model_verbose }}

Author: {{ cookiecutter.author_name }}
"""

import uuid as uuid
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import DateTimeField
from django_extensions.db.fields import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from django.apps import apps
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

from .managers import {{cookiecutter.model}}Manager as manager

class {{cookiecutter.model}}(models.Model):
    # === Basic ===
    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # === Identifiers ===
    name = models.CharField(max_length=150)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, editable=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    # === Properties ===
    

    # === State ===
    is_active = models.BooleanField(default=True)
    meta = JSONField(default=dict, blank=True, null=True)

    # === Relationship Fields ===
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='{{cookiecutter.module_plural}}_created_by_user'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='{{cookiecutter.module_plural}}_updated_by_user'
    )

    objects = manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = '{{cookiecutter.model_verbose}}'
        verbose_name_plural = '{{cookiecutter.model_verbose_plural}}'
    
    ################################################################################
    # === Magic Methods ===
    ################################################################################
    def __str__(self):
        return self.name    

    ################################################################################
    # === Model overrides ===
    ################################################################################
    def clean(self, *args, **kwargs):
        # add custom validation here
        super().clean()

    def save(self, *args, **kwargs):
        # self.full_clean()
        super().save(*args, **kwargs)

    ################################################################################
    # === Model-specific methods ===
    ################################################################################


################################################################################
# === Signals ===
################################################################################
@receiver(post_save, sender={{cookiecutter.model}})
def scaffold_post_save(sender, instance=None, created=False, **kwargs):
    pass


@receiver(pre_save, sender={{cookiecutter.model}})
def scaffold_pre_save(sender, instance=None, created=False, **kwargs):
    pass
