from django.contrib.auth.mixins import AccessMixin
from rest_framework.exceptions import PermissionDenied as APIPermissionDenied

from accounts.models.accounts.constants import USER, SUPERADMIN, ADMIN


class IsAdminAPIMixin(object):
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)

        try:
            if not request.user.user_type == ADMIN and not request.user.user_type == SUPERADMIN:
                raise APIPermissionDenied
        except AttributeError:
            raise APIPermissionDenied

        return dispatch


class IsAdminViewMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == ADMIN and not request.user.user_type == SUPERADMIN:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

