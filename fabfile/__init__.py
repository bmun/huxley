# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from fabric.api import env, hide, local, settings, task
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm
from os.path import abspath, dirname, join
from utils import git

env.huxley_root = abspath(dirname(dirname(__file__)))

@task
def feature(branch_name=None):
    '''Create a new feature branch.'''
    if not branch_name:
        print red('No branch name given. Usage: fab feature:<branch_name>')
        return
    git.new_branch(branch_name)

@task
def update():
    '''Rebase the current feature branch onto the latest version of upstream.'''
    print 'Updating your local branch...'
    git.pull()

@task
def test(*args):
    '''Run the project's test suite, with optionally specified apps.'''
    with hide('aborts', 'warnings'):
        return local('python manage.py test %s' % ' '.join(args))

@task
def authors():
    '''Update the AUTHORS file.'''
    authors = join(env.huxley_root, 'AUTHORS')
    with hide('running'):
        local('git log --format="%aN <%aE>" | sort -u > {0}'.format(authors))
        if local('git diff --name-only AUTHORS', capture=True):
            print green('Automatically updating the authors file...')
            local('git commit -m "Update AUTHORS." {0}'.format(authors))

@task
def submit(remote='origin', skip_tests=False):
    '''Push the current feature branch and create/update pull request.'''
    if not skip_tests:
        with settings(warn_only=True):
            if test().failed:
                if confirm(yellow('Tests failed. Continue anyway?')):
                    print yellow('Ignoring failed tests. Be careful.')
                else:
                    print red('Terminating due to failed tests.')
                    return
            else:
                print green('Tests OK!')

    first_submission = not git.remote_branch_exists(remote=remote)
    git.pull()
    authors()
    git.push()

    if not first_submission:
        print green('Pull request sucessfully updated.')
    elif git.hub_installed():
        current_branch = git.current_branch()
        local('hub pull-request -b bmun:master -h %s -f' % current_branch)
        print green('Pull request successfully issued.')
    else:
        print green('Branch successfully pushed. Go to GitHub to issue a pull request.')

@task
def finish():
    '''Delete the current feature branch.'''
    prompt = yellow('This will delete your local and remote topic branches. '
                    'Make sure your pull request has been merged or closed. '
                    'Are you sure you want to finish this branch?')
    if not confirm(prompt):
        print red('Aborting.')
        return

    print green('Branch %s successfully cleaned up.' % git.cleanup())

try:
    from deploy import deploy
except ImportError:
    pass
