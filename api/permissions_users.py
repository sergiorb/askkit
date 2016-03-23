# -*- coding: utf-8 -*

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from ipware.ip import get_ip

from polls.models import Poll, Option, Vote


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow users edit their profile.
    """

    message = "This is not your profile (ಠ_ಠ)."

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj == request.user:
            return True
        else:
            raise PermissionDenied(self.message)
