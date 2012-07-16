#!/usr/bin/env python

import csv
import os
import sys
import codecs

# Sets Django environment variables
sys.path.append('/Users/williamchieng/huxley/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from cms.models import *

with open('committees.csv', 'rU') as f:
    reader = csv.reader(f)
    shortnames = reader.next()
    longnames = reader.next()
    
    # Create country object and add it to the dictionary.
    for pair in zip(shortnames, longnames):
        if not pair[0] == '':
            committee = Committee(name=pair[0], fullname=pair[1])
            committee.save()
    
    for row in reader:
        country = Country(name=row[0])
        country.save()
        print country
        for index in range(1, len(row) - 1):
            committee = Committee.objects.get(name=shortnames[index])
            if row[index] == 'X':
                assignment = Assignment(country=country, committee=committee)
                print assignment
                assignment.save()
                
                
                
