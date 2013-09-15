# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from fabric.api import local, prompt
from os.path import dirname, exists, join

UTILS_ROOT = dirname(__file__)

def get_username():
    username_file = join(UTILS_ROOT, '.username')
    if not exists(username_file):
        local('touch %s' % username_file)
        username = prompt('What is your GitHub username?')
        local('echo %s > %s' % (username, username_file))

    username = local('cat %s' % username_file, capture=True)
    return username