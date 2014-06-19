# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase)
from huxley.core.models import School

class SchoolListCreateTestCase(CreateAPITestCase):
    url_name = 'api:school_list'
    params = {'name': 'Berkeley Prep',
            'address': '1 BMUN way',
            'city': 'Oakland',
            'state': 'California',
            'zip_code': 94720,
            'country': 'USA',
            'primary_name': 'Kunal Mehta',
            'primary_email': 'KunalMehta@huxley.org',
            'primary_phone': '9999999999',
            'program_type': User.TYPE_ADVISOR}

    '''def test_duplicate_name(self):
        params = self.get_params()
        invalid_params = '''
