from django.contrib.auth.models import Group
from rest_framework import permissions

def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """
    message = 'Check if user is in the specified group.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        required_groups = getattr(view, "required_groups", [])

        # Return True if the user is in group or is staff.
        for group_name in required_groups:
            if is_in_group(request.user, group_name):
                return True

        # Return True if the user is staff (admin).
        if (request.user and request.user.is_staff):
            return True
        
        return False
