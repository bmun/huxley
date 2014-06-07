# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from huxley.api.serializers import UserSerializer
from huxley.utils.shortcuts import render_template


def index(request):
    user_dict = {};
    if request.user.is_authenticated():
        user_dict = UserSerializer(request.user).data

    context = {'user_json': json.dumps(user_dict).replace('</', '<\\/')}
    return render_template(request, 'www.html', context)
