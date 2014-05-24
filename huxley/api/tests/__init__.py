# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase


class GetAPITestCase(APITestCase):
    '''Provides a base implementation to test GET APIs. Classes that extend
    this must define a url_name class method, and can then use the
    get_response method to make a GET request and get the JSON response.'''

    url_name = None

    def get_url(self, object_id):
        if not self.url_name:
            raise NotImplementedError('url_name not defined.')
        return reverse(self.url_name, args=(object_id,))

    def get_response(self, object_id):
        url = self.get_url(object_id)
        return json.loads(self.client.get(url).content)
