# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from fabric.api import local, task
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm
from utils import git

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
def submit(remote='origin'):
    '''Push the current feature branch and create/update pull request.'''
    first_submission = not git.remote_branch_exists(remote=remote)
    git.pull()
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
