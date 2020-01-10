from django.db import models, IntegrityError
from django.apps import apps


class ProfileQuerySet(models.QuerySet):
    def males(self):
        return self.filter(gender__name__iexact='male')

    def females(self):
        return self.filter(gender__name__iexact='female')


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def males(self):
        return self.get_queryset().males()

    def females(self):
        return self.get_queryset().females()

    def create(self, *args, **kwargs):
        if 'account' in kwargs:
            try:
                profile = self.get(account=kwargs['account'])
                return profile
            except self.model.DoesNotExist:
                return super(ProfileManager, self).create(*args, **kwargs)
            except KeyError:
                return super(ProfileManager, self).create(*args, **kwargs)
        return super(ProfileManager, self).create(*args, **kwargs)


class GenderManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            return super().create(*args, **kwargs)
        except IntegrityError:
            return self.get(name=kwargs.get('name'))
