# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import html

from huxley.core.models import Assignment, Committee, Country, CountryPreference, Registration, School


class AssignmentAdmin(admin.ModelAdmin):

    search_fields = ('country__name', 'registration__school__name',
                     'committee__name', 'committee__full_name')

    def list(self, request):
        '''Return a CSV file containing the current country assignments.'''
        assignments = HttpResponse(content_type='text/csv')
        assignments[
            'Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)
        writer.writerow(['School', 'Committee', 'Country', 'Rejected'])

        for assignment in Assignment.objects.all().order_by(
                'registration__school__name', 'committee__name'):
            writer.writerow([
                assignment.registration.school, assignment.committee,
                assignment.country, assignment.rejected
            ])

        return assignments

    def load(self, request):
        '''Loads new Assignments.'''
        assignments = request.FILES
        reader = csv.reader(assignments['csv'])

        def get_model(model, name, cache):
            name = name.strip()
            if not name in cache:
                try:
                    cache[name] = model.objects.get(name=name)
                except model.DoesNotExist:
                    cache[name] = name
            return cache[name]

        def generate_assignments(reader):
            committees = {}
            countries = {}
            schools = {}

            for row in reader:
                if (row[0] == 'School' and row[1] == 'Committee' and
                        row[2] == 'Country'):
                    continue  # skip the first row if it is a header

                while len(row) < 3:
                    row.append(
                        "")  # extend the row to have the minimum proper num of columns

                if len(row) < 4:
                    rejected = False  # allow for the rejected field to be null
                else:
                    rejected = (
                        row[3].lower() == 'true'
                    )  # use the provided value if admin provides it

                committee = get_model(Committee, row[1], committees)
                country = get_model(Country, row[2], countries)
                school = get_model(School, row[0], schools)
                yield (committee, country, school, rejected)

        failed_rows = Assignment.update_assignments(
            generate_assignments(reader))
        if failed_rows:
            # Format the message with HTML to put each failed assignment on a new line
            messages.error(request, html.format_html(
                'Assignment upload aborted. These assignments failed:<br/>' +
                '<br/>'.join(failed_rows)))

        return HttpResponseRedirect(
            reverse('admin:core_assignment_changelist'))

    def stable_marriage(self, suitor_preferences, suitor_max_proposals,
                        ranking_of_suitors, accepter_max_proposals,
                        suitors_per_accept):
        """
        This finds a stable marriage where:
        (1) each suitor contains multiple individuals
        (2) each accepter accepts proposals from multiple suitors
        (3) each accepter takes a certain number of individuals per acceptance
        (4) all accepters have the same preference list
        (5) suitor preference lists do not contain every accepter
        (6) suitors stop proposing when they have proposed to their entire preference list
        (7) not all individuals may be matched at the end
        (8) not all accepters may be full at the end

        suitor_preferences: Mapping of suitor to their preference-ordered list of accepters.
        suitor_max_proposals: Mapping from a suitor to the number of individuals it contains.
        ranking_of_suitors: Maps suitors to their rank. Assumes each accepter has the same preference order for suitors.
        accepter_max_proposals: Mapping of accepters to total number of proposals htey can accept.
        suitors_per_accept: Mapping from accepter to the number of individuals taken per acceptance. 
        """
        suitor_n_accepted = {s: 0 for s in suitor_preferences}
        accepted_proposals = {a: [] for a in accepter_max_proposals}

        unstable = True
        while unstable:
            unstable = False
            for s in suitor_preferences:
                n_prefs = len(suitor_preferences[s])
                for n in range(n_prefs):
                    if suitor_max_proposals[s] <= 0: break
                    next_proposal = suitor_preferences[s].pop(0)
                    if suitors_per_accept[
                            next_proposal] > suitor_max_proposals[s]:
                        suitor_preferences[s].append(next_proposal)
                        continue
                    accepted_proposals[next_proposal].append(s)
                    suitor_max_proposals[s] -= suitors_per_accept[
                        next_proposal]

            for a in accepted_proposals:
                max_proposals = accepter_max_proposals[a]
                if len(accepted_proposals[a]) > max_proposals:
                    unstable = True
                    accepted_proposals[a].sort(
                        key=lambda s: ranking_of_suitors[s])
                    for s in accepted_proposals[a][max_proposals:]:
                        suitor_max_proposals[s] += suitors_per_accept[a]
                    accepted_proposals[a] = accepted_proposals[
                        a][:max_proposals]

        for a in accepter_max_proposals:
            accepter_max_proposals[a] -= len(accepted_proposals[a])

        return accepted_proposals, suitor_max_proposals, accepter_max_proposals

    def assign(self, request):
        '''Return a CSV file containing automated country assignments.'''
        registrations = Registration.objects.filter(
            is_waitlisted__exact=False).order_by('registered_at')
        committees = Committee.objects.all()
        assignments = Assignment.objects.all()

        final_assigments = {c: [] for c in committees}
        assigned = {c: [] for c in committees}
        delegation_sizes = {c: c.delegation_size for c in committees}

        # Start by assuming each registration and committee has all space available
        reg_unassigned = {
            r: r.num_beginner_delegates + r.num_intermediate_delegates +
            r.num_advanced_delegates
            for r in registrations
        }

        committee_unassigned = {c: c.countries.all().count()
                                for c in committees}

        # Set aside existing assignments
        for a in assignments:
            if a.registration is None: continue

            # Determine which countries are already assigned for each committee
            assigned[a.committee].append(a)

            # Reduce how much space is available per each registration and committee
            reg_unassigned[a.registration] -= a.committee.delegation_size
            committee_unassigned[a.committee] -= 1

            # Add existing assigments directly to the collection of final assignments
            final_assigments[a.committee].append(
                (a.registration, a.country, a.rejected))

        # Registrations are ranked by their registration time
        reg_ranking = {r: r.registered_at for r in registrations}

        # Registrations do not order committee preferences. For the sake of the algorithm, 
        # choose an arbitrary order for theirs preference lists.
        reg_committee_rankings = {r: [] for r in registrations}
        for r in registrations:
            for c in r.committee_preferences.all():
                reg_committee_rankings[r].append(c)

        # Find a stable marriage, determine how much space is left per each registration and committee
        accepted, reg_unassigned, committee_unassigned = self.stable_marriage(
            reg_committee_rankings, reg_unassigned, reg_ranking,
            committee_unassigned, delegation_sizes)

        # Fill remaining space per each registration; try to place in non-specialized committees first
        for r in reg_unassigned:
            for c in committee_unassigned:
                if not reg_unassigned[r]: break

                if not c.special and c.delegation_size <= reg_unassigned[r] and \
                   committee_unassigned[c] and r not in accepted[c]:
                    accepted[c].append(r)
                    committee_unassigned[c] -= 1
                    reg_unassigned[r] -= c.delegation_size

        for r in reg_unassigned:
            for c in committee_unassigned:
                if not reg_unassigned[r]: break

                if c.delegation_size <= reg_unassigned[r] and \
                   committee_unassigned[c] and r not in accepted[c]:
                    accepted[c].append(r)
                    committee_unassigned[c] -= 1
                    reg_unassigned[r] -= c.delegation_size

        # Within each committee, determine each registration's country assignment
        for c in accepted:
            if not len(accepted[c]): continue
            exclude_countries = set(map(lambda a: a.country, assigned[c]))

            # This is a 1-to-1 pairing, so we do not need to worry about multiple proposals/acceptances
            countries = c.countries.all()
            country_unassigned = {country: 1
                                  for country in countries
                                  if country.id not in exclude_countries}
            for country in exclude_countries:
                country_unassigned[country] = 0
            country_per_reg = {r: 1 for r in accepted[c]}

            # Consturct each registration's preference list
            reg_country_rankings = {r: [] for r in accepted[c]}
            for r in accepted[c]:
                for pref in CountryPreference.objects.filter(
                        registration__id=r.id):
                    if pref.country.id in exclude_countries or pref.country.id not in countries:
                        continue
                    reg_country_rankings[r].append(pref)
                reg_country_rankings[r].sort(key=lambda p: p.rank)
                reg_country_rankings[r] = map(lambda p: p.country,
                                              reg_country_rankings[r])

            country_pairing, country_per_reg, country_unassigned = self.stable_marriage(
                reg_country_rankings, country_per_reg, reg_ranking,
                country_unassigned, country_unassigned)

            # Handle the remaining pairings. By construction,
            # can assume number of unpaired countries equals
            # number of unpaired registrations
            for r in country_per_reg:
                if country_per_reg[r] > 0:
                    for country in country_unassigned:
                        if country_unassigned[country]:
                            country_pairing[country] = [r]
                            country_unassigned[country] = 0
                            country_per_reg[r] = 0
                            break

            # No further work needs to be done for these assignments
            for country in country_pairing:
                if not len(country_pairing[country]): continue
                final_assigments[c].append(
                    (country_pairing[country][0], country, False))

        # Format and write results to CSV
        to_write = []
        for committee in final_assigments:
            if not len(final_assigments[committee]): continue
            for assignment in final_assigments[committee]:
                registration, country, rejected = assignment

                # External likes the number of lines in the CSV to equal the number of delegates
                for n in range(committee.delegation_size):
                    to_write.append((registration.school.name, committee.name,
                                     country.name, rejected))

        to_write.sort(key=lambda row: row[0] + row[1] + row[2])

        assignments = HttpResponse(content_type='text/csv')
        assignments[
            'Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)
        writer.writerow(['School', 'Committee', 'Country', 'Rejected'])

        for line in to_write:
            writer.writerow(line)

        return assignments

    def get_urls(self):
        return super(AssignmentAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_assignment_list'),
            url(r'assign',
                self.admin_site.admin_view(self.assign),
                name='core_assignment_assign'),
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_assignment_load', ),
        ]
