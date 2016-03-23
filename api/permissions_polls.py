# -*- coding: utf-8 -*

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from ipware.ip import get_ip

from polls.models import Poll, Option, Vote


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


class OnlyOneVote(permissions.BasePermission):
    """
    Object-level permission to only allow one vote per user/ip.
    """

    message = "You have already voted this poll."

    def  has_object_permission(self, request, view, obj):

        if request.user.is_authenticated():

            option = Option.objects.select_related('poll').get(pk=obj.pk)
            options = option.poll.options.all()

            vote = Vote.objects.filter(option__in=options, user=request.user)

            if len(vote) == 0:
                return True
            else:
                raise PermissionDenied(self.message)

            return True
        else:

            option = Option.objects.select_related('poll').get(pk=obj.pk)
            options = option.poll.options.all()
            
            vote = Vote.objects.filter(option__in=options, fromIp=get_ip(request))

            if len(vote) == 0:
                return True
            else:
                self.message = 'Your IP has already voted this poll.'
                raise PermissionDenied(self.message)
