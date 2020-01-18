from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import Account
from .models.account.admin import UserAdmin

# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
