from rest_framework.permissions import BasePermission


ROLE_GROUPS = {
    'superadmin': {'SuperAdmin'},
    'ops': {'Ops'},
    'instructor': {'Instructor'},
    'support': {'Support'},
}


def _user_roles(user):
    if not user or not user.is_authenticated:
        return set()
    names = set(user.groups.values_list('name', flat=True))
    roles = set()
    for role, groups in ROLE_GROUPS.items():
        if names & groups:
            roles.add(role)
    if user.is_superuser:
        roles.add('superadmin')
    return roles


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return 'superadmin' in _user_roles(request.user)


class IsOps(BasePermission):
    def has_permission(self, request, view):
        roles = _user_roles(request.user)
        return 'ops' in roles or 'superadmin' in roles


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        roles = _user_roles(request.user)
        return 'support' in roles or 'superadmin' in roles


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        roles = _user_roles(request.user)
        return 'instructor' in roles or 'superadmin' in roles

