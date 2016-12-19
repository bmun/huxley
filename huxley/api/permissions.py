# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.http import QueryDict
from rest_framework import permissions

from huxley.core.models import Assignment, Delegate


class IsSuperuserOrReadOnly(permissions.BasePermission):
    '''Allow writes if superuser, read-only otherwise.'''

    def has_permission(self, request, view):
        return (request.user.is_superuser or
                request.method in permissions.SAFE_METHODS)


class IsUserOrSuperuser(permissions.BasePermission):
    '''Accept only the users themselves or superusers.'''

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj


class IsAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the school's advisor or superusers.'''

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.advisor


class IsChairOrSuperuser(permissions.BasePermission):
    '''Accept only the committee's chair or superusers.'''

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.chair


class IsSchoolAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the advisor of the given school_id query param.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        school_id = view.kwargs.get('pk', None)
        user = request.user

        return (user.is_authenticated() and user.is_advisor() and
                user.school_id == int(school_id))


class IsPostOrSuperuserOnly(permissions.BasePermission):
    '''Accept POST (create) requests, superusers-only otherwise.'''

    def has_permission(self, request, view):
        return request.method == 'POST' or request.user.is_superuser


class IsSchoolAssignmentAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the advisor of the given school with a given assignment.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        assignment_id = view.kwargs.get('pk', None)
        assignment = Assignment.objects.get(id=assignment_id)
        user = request.user

        return (user.is_authenticated() and user.is_advisor() and
                user.school.id == assignment.school.id)


class IsSchoolDelegateAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the advisor of the given school with a given assignment.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        delegate_id = view.kwargs.get('pk', None)
        delegate = Delegate.objects.get(id=delegate_id)
        user = request.user

        return (user.is_authenticated() and user.is_advisor() and
                user.school.id == delegate.school.id)


class AssignmentListPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return user_is_advisor(request, view)

        return False


class DelegateListPermission(permissions.BasePermission):
    '''Accept requests to create, get and update delegates in bulk from
       the superuser and from the advisor of the school of the delegates.'''

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True

        method = request.method
        if method in permissions.SAFE_METHODS:
            return user_is_advisor(request, view)

        if method in ('POST', 'PUT', 'PATCH'):
            school_id = user.is_authenticated() and user.school_id
            if not school_id:
                return False

            if method == 'POST':
                return int(request.data['school']) == school_id
            else:
                delegate_ids = [delegate['id'] for delegate in request.data]
                return not Delegate.objects.filter(id__in=delegate_ids).exclude(school_id=school_id).exists()

        return False


def user_is_advisor(request, view):
    user = request.user
    school_id = request.GET.get('school_id', -1)
    return user.is_authenticated() and user.school_id == int(school_id)
