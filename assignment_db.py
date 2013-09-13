import os

os.environ['PYTHONPATH'] = os.path.abspath('PYTHONPATH')
os.environ['DJANGO_SETTINGS_MODULE'] = 'huxley.settings'

from huxley.core.models import Country, Committee, Assignment
from xlrd import open_workbook

s = open_workbook('Country Matrix.xlsx').sheet_by_index(0)

country_range = s.nrows-2
committee_range = 21

for row in range(2, country_range):
	Country.objects.get_or_create(name=s.cell(row, 0).value, special=(True if row > 204 else False))

for col in range(1, committee_range):
	Committee.objects.get_or_create(name=s.cell(1, col).value, delegation_size=(1 if s.cell(0, col).value == 'SINGLE' else 2), special=(True if col > 15 else False))

for row in range(2, country_range):
	for col in range(1, committee_range):
		if s.cell(row, col).value:
			print s.cell(1, col).value
			print s.cell(row, 0).value
			print s.cell(row,col).value
			print
			country_name = Country.objects.get(name=s.cell(row, 0).value)
			committee_name = Committee.objects.get(name=s.cell(1, col).value)
			assignment = Assignment(committee=committee_name, country=country_name)
			assignment.save()

