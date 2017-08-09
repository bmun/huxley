# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.http import QueryDict
from rest_framework import permissions

from huxley.core.models import Assignment, Delegate, Registration


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


class IsSchoolAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the advisor of the given school_id query param.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        school_id = view.kwargs.get('pk', None)
        user = request.user

        return user_is_advisor(request, view, school_id)


class IsPostOrSuperuserOnly(permissions.BasePermission):
    '''Accept POST (create) requests, superusers-only otherwise.'''

    def has_permission(self, request, view):
        return request.method == 'POST' or request.user.is_superuser


class RegistrationListPermission(permissions.BasePermission):
    '''Accept only when the school of the registration object is the same
       as the school of the user, or is a post, or is the superuser.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'POST':
            return True

        if request.method in permissions.SAFE_METHODS:
            school_id = request.query_params.get('school_id', -1)
            return user_is_advisor(request, view, school_id)

        return False


class IsSchoolAssignmentAdvisorOrSuperuser(permissions.BasePermission):
    '''Accept only the advisor of the given school with a given assignment.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        assignment_id = view.kwargs.get('pk', None)
        assignment = Assignment.objects.get(id=assignment_id)
        user = request.user

        return user_is_advisor(request, view,
                               assignment.registration.school_id)


class AssignmentDetailPermission(permissions.BasePermission):
    '''Accept requests to retrieve an assignment from superusers, the advisor of 
       the assignment's school, and delegates with the requested assignment.
       Onyl allow superusers to update assignments.'''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        assignment_id = view.kwargs.get('pk', None)
        assignment = Assignment.objects.get(id=assignment_id)
        user = request.user
        method = request.method

        if method == 'GET':
            return (user_is_advisor(request, view, assignment.school_id) or
                    user_is_delegate(request, view, assignment_id))

        return False


class AssignmentListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            school_id = request.query_params.get('school_id', -1)
            committee_id = request.query_params.get('committee_id', -1)
            return (user_is_chair(request, view, committee_id) or
                    user_is_advisor(request, view, school_id))

        return False


class DelegateDetailPermission(permissions.BasePermission):
    '''Accept requests to retrieve, update, and destroy a delegate from the
       superuser and the advisor of the school of the delegate. Accept requests
       to retrieve and update a delegate from the chair of the committee of
       the delegate.'''

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True

        delegate_id = view.kwargs['pk']
        delegate = Delegate.objects.get(id=delegate_id)

        if user_is_advisor(request, view, delegate.school_id):
            return True

        if (delegate.assignment and
                user_is_chair(request, view, delegate.assignment.committee_id)
                and request.method != 'DELETE'):
            return True

        return False


class DelegateListPermission(permissions.BasePermission):
    '''Accept requests to create, retrieve, and update delegates in bulk from
       the superuser and from the advisor of the school of the delegates.
       Accept requests to retrieve and update delegates from the chair of the
       committee of the delegates.'''

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True

        if not user.is_authenticated():
            return False

        method = request.method
        if method in permissions.SAFE_METHODS:
            school_id = request.query_params.get('school_id', -1)
            committee_id = request.query_params.get('committee_id', -1)
            return (user_is_chair(request, view, committee_id) or
                    user_is_advisor(request, view, school_id))

        if method == 'POST':
            return user_is_advisor(request, view, request.data['school'])

        if method in ('PUT', 'PATCH'):
            delegate_ids = [delegate['id'] for delegate in request.data]
            delegates = Delegate.objects.filter(id__in=delegate_ids)
            if user.is_chair():
                return not delegates.exclude(
                    assignment__committee_id=user.committee_id).exists()

            if user.is_advisor():
                return not delegates.exclude(school_id=user.school_id).exists()

        return False
        

class SchoolDetailPermission(permissions.BasePermission):
    '''Accept only the school's advisor, the school's delegates, or 
       superusers to retrieve the school. Accept only superusers and the advisor
       to update the school.'''

    def has_permission(self, request, view):
        user = request.user
        method = request.method
        school_id = view.kwargs.get('pk', None)

        if method == 'GET':
            return (user_is_advisor(view, request, school_id),
                    user_is_school_delegate(view, request, school_id))

        return user.is_superuser or user_is_advisor(view, request, school_id)


def user_is_advisor(request, view, school_id):
    user = request.user
    return (user.is_authenticated() and user.is_advisor() and
            user.school_id == int(school_id))


def user_is_chair(request, view, committee_id):
    user = request.user
    return (user.is_authenticated() and user.is_chair() and
            user.committee_id == int(committee_id))

def user_is_delegate(request, view, assignment_id):
    user = request.user
    return (user.is_authenticated() and user.is_delegate() and
            user.assignment_id == int(assignment_id))

def user_is_school_delegate(request, view, school_id):
    user = request.user
    assignment_id = user.assignment_id
    assignment = Assignment.objects.get(id=assignment_id)
    return (user.is_authenticated() and user.is_delegte() and
            assignment.school_id = int(school_id))
