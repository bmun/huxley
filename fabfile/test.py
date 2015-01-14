# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from os.path import join

from fabric.api import env, hide, lcd, local, task


@task(default=True)
def run():
    '''Run the test suites and return a boolean indicating success.'''
    # TODO: Only run a language's tests if there have been changes in that
    # language.
    return python() and js()


@task
def python(*args):
    '''Run the python test suite, with optionally specified apps.'''
    with hide('aborts', 'warnings'), lcd(env.huxley_root):
        dirs = [join(env.huxley_root, 'huxley', arg) for arg in args]
        return not local('python manage.py test ' + ' '.join(dirs)).failed


@task
def js():
    '''Run the JS test suite.'''
    with hide('aborts', 'warnings'), lcd(env.huxley_root):
        return not local('npm test').failed
