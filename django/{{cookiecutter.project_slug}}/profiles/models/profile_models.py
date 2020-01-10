from django.contrib.postgres.forms import JSONField
from django.db import models, IntegrityError
from django_extensions.db import fields as extension_fields

from profiles.models.managers import ProfileManager, GenderManager


class Gender(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    objects = GenderManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Profile(models.Model):
    # Fields
    first_name = models.CharField(max_length=32, blank=True, null=True, default='')
    middle_name = models.CharField(max_length=32, blank=True, null=True, default='')
    last_name = models.CharField(max_length=32, blank=True, null=True, default='')
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    created = models.DateTimeField(null=False, auto_now_add=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    # Relationship Fields
    gender = models.ForeignKey(Gender, related_name='gender_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    account = models.OneToOneField(
        'accounts.Account',
        on_delete=models.CASCADE,
    )

    meta = JSONField()

    objects = ProfileManager()

    class Meta:
        ordering = ('account', '-created')

    def __str__(self):
        return self.get_full_name()

    def as_html(self):
        html = f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Full Name</span><span class='kv-value'>{self.get_full_name()}</p>" \
            f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Sex</span><span class='kv-value'>{self.gender}</p>" \
            f"<p class='kv-pair kv-pair-center'><span class='kv-key'>Date of Birth</span><span class='kv-value'>{self.date_of_birth}</p>"
        return html

    def get_casual_name(self):
        if self.first_name != '':
            return self.first_name
        return 'Unnamed'

    def get_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{} {}'.format(
                self.first_name, self.last_name
            )
        else:
            if self.account.username is not None:
                return self.account.username
            return self.account.email

    def get_full_name(self):
        if self.first_name != '' and self.last_name != '':
            return '{}, {}'.format(
                self.last_name, self.first_name
            )
        else:
            try:
                if self.account.username is not None:
                    return self.account.username
            except AttributeError:
                return 'Unnamed'
            return 'Unnamed'
