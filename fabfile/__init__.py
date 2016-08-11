# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from os.path import abspath, dirname, join

from fabric.api import abort, hide, env, execute, local, settings, task
from fabric.contrib.console import confirm

from yapf.yapflib.yapf_api import FormatFile

from . import dependencies, migrations, pr, test
from .utils import git, ui

env.huxley_root = abspath(dirname(dirname(__file__)))
env.js_root = join(env.huxley_root, 'huxley/www/static/js')


@task
def feature(branch_name=None):
    '''Create a new feature branch.'''
    if branch_name:
        git.new_branch(branch_name)
        dependencies.check()
        migrations.check()
    else:
        print ui.error(
            'No branch name given. Usage: fab feature:<branch_name>')


@task
def update():
    '''Rebase the current feature branch onto the latest version of upstream.'''
    print ui.info('Updating your local branch...')
    git.pull()
    print ui.info('Clearing old files...')
    local('git clean -xf *.css')
    dependencies.check()
    migrations.check()


@task
def format():
    '''Format and commit python files committed on the current feature branch'''
    diff_list = git.diff_name_only()
    py_diff_list = [pyfile for pyfile in diff_list if pyfile[-3:] == '.py']

    if confirm('Review formatting changes? (Select no to approve all)'):
        for pyfile in py_diff_list:
            print('\n')
            for line in FormatFile(pyfile, print_diff=True):
                print(line)
            if confirm('Accept changes to %s?' % pyfile):
                FormatFile(pyfile, in_place=True)
    else:
        for pyfile in py_diff_list:
            FormatFile(pyfile, in_place=True)
    print ui.info('Formatting complete')

    if len(local('git status --porcelain', capture=True)) > 0:
        local('git add --all')
        local('git commit -m "Ran autoformatter"')


@task
def submit(remote='origin', skip_tests=False):
    '''Push the current feature branch and create/update pull request.'''
    execute(format)
    if not skip_tests:
        with settings(warn_only=True):
            if not test.run():
                if confirm(ui.warning('Tests failed. Continue anyway?')):
                    print ui.warning('Ignoring failed tests. Be careful.')
                else:
                    print ui.error('Terminating due to failed tests.')
                    return
            else:
                print ui.success('Tests OK!')

    first_submission = not git.remote_branch_exists(remote=remote)
    git.pull()
    git.push()

    if not first_submission:
        print ui.success('Pull request sucessfully updated.')
    elif git.hub_installed():
        current_branch = git.current_branch()
        local('hub pull-request -b bmun:master -h %s -f' % current_branch)
        print ui.success('Pull request successfully issued.')
    else:
        print ui.success(
            'Branch successfully pushed. Go to GitHub to issue a pull request.')


@task
def finish(branch_name=None, remote='origin'):
    '''Delete the current feature branch.'''
    prompt = ui.warning(
        'This will delete your local and remote topic branches. '
        'Make sure your pull request has been merged or closed. '
        'Are you sure you want to finish this branch?')
    if not confirm(prompt):
        abort('Branch deletion canceled.')

    print ui.success('Branch %s successfully cleaned up.' %
                     git.cleanup(branch_name, remote))


try:
    from deploy import deploy, restart
except ImportError:
    pass
