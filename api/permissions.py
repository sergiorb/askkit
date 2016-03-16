from rest_framework import permissions

class AnonVotingForOptions(permissions.BasePermission):
    """
    Object-level permission to only allow anon votes on options that allow it.
    """

    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):

        if obj.poll.anon_allowed:
            return True
        elif request.user.is_authenticated():
            return True
        else:
            return False

class OptionNotOwner(permissions.BasePermission):
    """
    Object-level permission to don't allow object owners performs actions to 
    it.
    """

    message = "You can't vote your own polls."

    def has_object_permission(self, request, view, obj):

        return not obj.poll.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user