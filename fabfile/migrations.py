# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from fabric.api import env, hide, lcd, local, task
from fabric.colors import cyan, green, yellow


@task
def check():
    with lcd(env.huxley_root), hide('running'):
        print cyan('Checking migration status...')
        rows = local('./manage.py migrate --list', capture=True).split('\n')
        unapplied = filter(lambda r: r.startswith('  ( '), rows)

        if not unapplied:
            print green('Migrations are up-to-date.')
            return

        print yellow('Unapplied Migrations:')
        for migration in unapplied:
            print migration[5:]
        print yellow('To apply migrations, '
                     'run `python manage.py migrate <appname>`.\n'
                     '(For us, <appname> is usually core.)')
