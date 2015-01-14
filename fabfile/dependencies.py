# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from os.path import join

from fabric.api import abort, env, hide, lcd, local, task
from fabric.contrib.console import confirm

from .utils import ui


@task(default=True)
def check(lang='all'):
    '''Check installed dependencies against the requirements files.'''
    if lang in ('python', 'py', 'all'):
        check_python()
    if lang in ('js', 'all'):
        check_js()


@task
def update(lang='all'):
    '''Update dependencies based on the requirements files.'''
    if lang in ('python', 'py', 'all'):
        update_python()
    if lang in ('js', 'all'):
        update_js()


def check_python():
    '''Check/update the installed dependencies against requirements.txt.'''
    print ui.info('Checking python dependencies...')

    with open(join(env.huxley_root, 'requirements.txt'), 'r') as f:
        requirements = f.read()
    with hide('running'):
        installed = local('pip freeze', capture=True)

    def parse(text):
        pairs = map(lambda l: l.split('=='), text.strip().split('\n'))
        return {pair[0]: pair[1] for pair in pairs}

    expected, actual = parse(requirements), parse(installed)
    if not check_versions(expected, actual):
        if confirm('Update dependences?'):
            update_python()


def update_python():
    '''Update python dependences with pip.'''
    print 'Updating python dependencies...'
    with lcd(env.huxley_root):
        local('pip install -r requirements.txt')


def check_js():
    '''Check the installed dependencies against package.json.'''
    print ui.info('Checking JS dependencies...')
    with hide('running'):
        if not local('which npm', capture=True):
            print ui.error('npm not found! Install it with `brew install npm`.')
            return

    with open(join(env.huxley_root, 'package.json'), 'r') as p:
        package = json.loads(p.read())
        required = package['dependencies']
    with lcd(env.huxley_root), hide('running'):
        npm_list = json.loads(local('npm list --json', capture=True))
        modules = npm_list.get('dependencies', {}).items()
        installed = {name: info['version'] for name, info in modules}

    if not check_versions(required, installed):
        if confirm('Update dependencies?'):
            update_js()


def update_js():
    '''Update JS dependencies with npm.'''
    print 'Updating JS dependencies...'
    with lcd(env.huxley_root):
        local('npm install')


def check_versions(expected, actual):
    '''Check module versions and print a table of mismatches.'''
    if all(actual.get(name) == version for name, version in expected.items()):
        print ui.success('Dependencies are up-to-date.')
        return True

    print ui.warning('Dependencies are out of date!')
    row_format ="{:<25}" * 3
    print '\n', row_format.format('module', 'required', 'installed')
    print row_format.format('------', '--------', '---------')

    for module in sorted(expected.keys()):
        expected_version = expected[module]
        actual_version = actual.get(module, ui.warning('none'))
        if expected_version != actual_version:
            print row_format.format(module, expected_version, actual_version)

    print row_format.format('------', '--------', '---------'), '\n'
    return False

