# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import os
from os import environ
from os.path import abspath, dirname
import sys

sys.path.append(abspath(dirname(dirname(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'huxley.settings'

from huxley.core.models import Country, Committee, Assignment
from xlrd import open_workbook

s = open_workbook('Country Matrix.xlsx').sheet_by_index(0)

country_range = s.nrows
committee_range = 22

for row in range(3, country_range):
	Country.objects.get_or_create(name=s.cell(row, 0).value, special=(True if row > 154 else False))

for col in range(1, committee_range):
	Committee.objects.get_or_create(name=s.cell(1, col).value, full_name=s.cell(2, col).value, delegation_size=(1 if s.cell(0, col).value == 'SINGLE' else 2), special=(True if (col > 13 and col != 21) else False))

for row in range(3, country_range):
	for col in range(1, committee_range):
		if s.cell(row, col).value:
			print s.cell(1, col).value
			print s.cell(2, col).value
			print s.cell(row, 0).value
			print s.cell(row,col).value
			print
			country = Country.objects.get(name=s.cell(row, 0).value)
			committee = Committee.objects.get(name=s.cell(1, col).value)
			assignment = Assignment(committee=committee, country=country)
			assignment.save()

