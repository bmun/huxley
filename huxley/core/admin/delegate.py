# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from datetime import datetime


from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.base_user import BaseUserManager

from django.core.mail import send_mail
from django.core.validators import EmailValidator, ValidationError

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from googleapiclient.discovery import build
from google.oauth2 import service_account

from huxley.core.models import Assignment, Committee, Delegate
from huxley.accounts.models import User


class DelegateAdmin(admin.ModelAdmin):

    search_fields = ('name', )
    actions = ['create_accounts_for_selected']

    def get_rows(self):
        rows = []

        rows.append([
            'ID', 'Name', 'Committee', 'Country', 'Email'
        ])

        ordering = 'name'
        for delegate in Delegate.objects.all().order_by(ordering):
            rows.append([
                str(delegate.id),
                str(delegate),
                str(delegate.committee),
                str(delegate.country),
                str(delegate.email)
            ])
        return rows

    def roster(self, request):
        '''Return a CSV file representing the entire roster of registered
        delegates, including their committee, country, and school.'''
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="roster.csv"'
        writer = csv.writer(roster)
        for row in self.get_rows():
            writer.writerow(row)

        return roster

    def load(self, request):
        '''
        Loads new Assignments and/or updates assignments.
        CSV format: Name, Committee, Country, Email"
        '''
        validator = EmailValidator()

        existing_delegates = Delegate.objects.all()
        delegates = request.FILES
        reader = csv.reader(
            delegates['csv'].read().decode('utf-8').splitlines())
        assignments = {}
        for assignment in Assignment.objects.all():
            assignments[(assignment.committee.name,
                         assignment.country.name)] = assignment
        failed_rows = []
        for row in reader:
            if row and row[0] != 'Name':
                assignment_check = (str(row[1]), str(row[2])) in assignments
                email_check = True
                try:
                    validator(str(row[3]))
                except ValidationError:
                    email_check = False

                if assignment_check and email_check:
                    assignment = assignments.get((str(row[1]), str(row[2])))
                    email = str(row[3])
                    delg = list(
                        Delegate.objects.filter(name=str(row[0]), email=email))
                    if len(delg) == 1:
                        Delegate.objects.filter(name=str(
                            row[0]), email=email).update(assignment=assignment)
                    else:
                        Delegate.objects.create(name=row[0],
                                                email=email,
                                                assignment=assignment)
                else:
                    failed_rows.append(row)
        if failed_rows:
            messages.error(
                request, 'Not all delegates could upload. These rows failed because the committee could not be matched or email was invalid: '
                + str(failed_rows))

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Delegates!A1:K'
            # Store credentials
            creds = service_account.Credentials.from_service_account_file(
                settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES)

            service = build('sheets', 'v4', credentials=creds)

            response = service.spreadsheets().values().get(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                majorDimension='ROWS').execute()

            if 'values' in response and len(response['values']) > 1:
                for row in response['values'][1:]:
                    if Delegate.objects.filter(id=row[0]):
                        delegate = Delegate.objects.get(id=row[0])
                        if row[6] == "TRUE" or row[6] == "x":
                            delegate.waiver_submitted = True
                            delegate.save()

            data = self.get_rows()

            body = {
                'values': data,
            }
            response = service.spreadsheets().values().clear(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
            ).execute()
            service.spreadsheets().values().update(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                valueInputOption='USER_ENTERED',
                body=body).execute()

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def confirm_waivers(self):
        # TODO THIS DOESNT MAKE ANY SENSE WHY IS THE METHOD STILL BEING CALLED
        return

    def create_accounts_for_selected(self, request, queryset):
        created = 0
        for delegate in queryset:
            # Buffer so we only allow up to 50 emails to be sent at a time
            if created == 50:
                break
            if not User.objects.filter(delegate__id=delegate.id).exists():
                names = delegate.name.split(' ')
                username = names[0] + '_' + str(delegate.id)
                password = BaseUserManager().make_random_password(10)
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    delegate=delegate,
                    user_type=User.TYPE_DELEGATE,
                    first_name=delegate.name.split()[0],
                    last_name=delegate.name.split()[-1],
                    email=delegate.email,
                    last_login=datetime.now())
                send_mail('BMUN Fall Conference Account Created For {0}'.format(delegate.name),
                          'Username: {0}\n'.format(username)
                          + 'Password: {0}\n'.format(password)
                          + 'Welcome to Berkeley Model United Nations! \n'
                          + 'Please save these details to login to your Huxley Notes account '
                          + 'for Fall Conference 2021. You will need it send notes. '
                          + 'during the conference. You can access '
                          + 'this account at notes.huxley.bmun.org.',
                          'no-reply@bmun.org',
                          [delegate.email], fail_silently=True)
                created += 1
        messages.info(request, "Created %s accounts" % str(created))

    def create_accounts(self, request):
        '''
        Create an account for every delegate object that do not have yet accounts 
        and send emails with account details
        '''
        # for delegate in Delegate.objects.all():
        #     if not User.objects.filter(delegate__id=delegate.id).exists():
        #         username = delegate.name + "_" + str(delegate.id)
        #         password = BaseUserManager().make_random_password(10)
        #         user = User.objects.create_user(
        #             username=username,
        #             password=password,
        #             delegate=delegate,
        #             user_type=User.TYPE_DELEGATE,
        #             first_name=delegate.name.split()[0],
        #             last_name=delegate.name.split()[-1],
        #             email=delegate.email,
        #             last_login=datetime.now())

        #         send_mail('BMUN Fall Conference Account Created For {0}'.format(delegate.name),
        #                   'Username: {0}\n'.format(username)
        #                   + 'Password: {0}\n'.format(password)
        #                   + 'Welcome to Berkeley Model United Nations! \n'
        #                   + 'Please save these details to login to your Huxley Notes account '
        #                   + 'for Fall Conference 2021. You will need it send notes. '
        #                   + 'during the conference. You can access '
        #                   + 'this account at notes.huxley.bmun.org.',
        #                   'no-reply@bmun.org',
        #                   [delegate.email], fail_silently=True)
        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def get_urls(self):
        return super(DelegateAdmin, self).get_urls() + [
            url(
                r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster',
            ),
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_delegate_load',
            ),
            url(
                r'confirm_waivers',
                self.admin_site.admin_view(self.confirm_waivers),
                name='core_delegate_confirm_waivers',
            ),
            url(
                r'sheets',
                self.admin_site.admin_view(self.sheets),
                name='core_delegate_sheets',
            ),
            url(
                r'create_accounts',
                self.admin_site.admin_view(self.create_accounts),
                name='core_delegate_create_accounts',
            )
        ]
