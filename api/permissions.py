# -*- coding: utf-8 -*

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a POLL to edit it.
    """

    message = "This poll doesn't belong to you."

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == request.user:
            return True
        else:
            raise PermissionDenied(self.message)


class OptionIsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow option's owner to update or deletes
    it.
    """

    message = "This options doesn't belong to you."

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if obj.poll.owner == request.user:
            return True
        else:
            raise PermissionDenied(self.message)


class AnonVotingForOptions(permissions.BasePermission):
    """
    Object-level permission to only allow anon votes on options that allow it.
    """

    message = "This poll doesn't allow anonymous votes. (⌐■_■)"

    def has_object_permission(self, request, view, obj):

        if obj.poll.anon_allowed:
            return True
        elif request.user.is_authenticated():
            return True
        else:
            raise PermissionDenied(self.message)


class VotingInTime(permissions.BasePermission):
    """
     Object-level permission to only allow votes between poll.date_begin and
     poll.date_end (if exists).
    """

    message = "Votation out of date."

    def has_object_permission(self, request, view, obj):

        if obj.poll.is_active():
            return True
        else:
            raise PermissionDenied(self.message)


class VoterNotOwner(permissions.BasePermission):
    """
    Object-level permission to don't allow options owners vote theirself.
    """

    message = "You can't vote your own polls."

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated():

            if obj.poll.owner == request.user:
                raise PermissionDenied(self.message)
            else:
                return True
        else:
            return True
