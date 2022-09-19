from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    '''
        we overwrite this
        the owner of object that we want to access should be the request.user
    '''
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user