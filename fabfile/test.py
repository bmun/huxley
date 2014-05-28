# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from os.path import join

from fabric.api import env, hide, lcd, local, task


@task(default=True)
def run():
    '''Run the project's python and JS test suites.'''
    # TODO: Only run a language's tests if there have been changes in that
    # language.
    python()
    js()


@task
def python(*args):
    '''Run the python test suite, with optionally specified apps.'''
    with hide('aborts', 'warnings'), lcd(env.huxley_root):
        dirs = [join(env.huxley_root, 'huxley', arg) for arg in args]
        return local('python manage.py test ' + ' '.join(dirs))


@task
def js():
    '''Run the JS test suite.'''
    with hide('aborts', 'warnings'), lcd(env.js_root):
        return local('npm test')
