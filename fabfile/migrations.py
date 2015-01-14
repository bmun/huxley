# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from fabric.api import env, hide, lcd, local, task

from .utils import ui


@task
def check():
    with lcd(env.huxley_root), hide('running'):
        print ui.info('Checking migration status...')
        rows = local('./manage.py migrate --list', capture=True).split('\n')
        unapplied = filter(lambda r: r.startswith('  ( '), rows)

        if not unapplied:
            print ui.success('Migrations are up-to-date.')
            return

        print ui.warning('Unapplied Migrations:')
        for migration in unapplied:
            print migration[5:]
        print ui.warning('To apply migrations, '
                     'run `python manage.py migrate <appname>`.\n'
                     '(For us, <appname> is usually core.)')
