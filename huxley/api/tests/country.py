# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.core.models import Country
from huxley.utils.test import TestCountries, TestUsers


class CountryDetailGetTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def get_url(self, country_id):
		return reverse('api:country_detail', args=(country_id,))

	def get_response(self, url):
		return json.loads(self.client.get(url).content)

	def test_anonymous_user(self):
		'''Fields should be returned when accessed by any user.'''
		country = TestCountries.new_country()
		url = self.get_url(country.id)
		response = self.get_response(url)
		self.assertEqual(response['name'], country.name)
		self.assertEqual(response['special'], country.special)

class CountryListGetTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.url = reverse('api:country_list')

	def get_data(self):
		return json.loads(self.client.get(self.url).content)

	def test_anonymous_user(self):
		'''Anyone should be able to access a list of all the countries.'''
		country1 = TestCountries.new_country(name='USA')
		country2 = TestCountries.new_country(name='China')
		country3 = TestCountries.new_country(name='Barbara Boxer', special=True)
		data = self.get_data()
		self.assertEqual(data[0],
						 {'id': country1.id,
						  'special': country1.special,
						  'name': country1.name})
		self.assertEqual(data[1],
						 {'id': country2.id,
						  'special': country2.special,
						  'name': country2.name})
		self.assertEqual(data[2],
						 {'id': country3.id,
						  'special': country3.special,
						  'name': country3.name})
