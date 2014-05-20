# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.core.models import Country
from huxley.utils.test import TestCountries

class CountryDetailGetTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def get_url(self, country_id):
		return reverse('api:country_detail', args=(country_id,))

	def get_response(self, url):
		return json.loads(self.client.get(url).content)

	def test_anonymous_user(self):
		'''Fields for this country should be returned'''
		country = TestCountries.new_country()
		url = self.get_url(country.id)
		response = self.get_response(url)

		assertEqual(response['name'], country.name)
		assertEqual(response['special'], country.special)




