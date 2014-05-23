# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json
import urllib2

from os.path import abspath, dirname, join

from fabric.api import abort, env, hide, local, settings, task
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm

from . import dependencies
from .utils import git


env.huxley_root = abspath(dirname(dirname(__file__)))
env.js_root = join(env.huxley_root, 'huxley/www/static/js')


@task
def feature(branch_name=None):
    '''Create a new feature branch.'''
    if branch_name:
        git.new_branch(branch_name)
        dependencies.check()
    else:
        print red('No branch name given. Usage: fab feature:<branch_name>')


@task
def update():
    '''Rebase the current feature branch onto the latest version of upstream.'''
    print 'Updating your local branch...'
    git.pull()
    dependencies.check()


@task
def test(*args):
    '''Run the project's test suite, with optionally specified apps.'''
    with hide('aborts', 'warnings'):
        result = [join(env.huxley_root, 'huxley', arg) for arg in args]
        return local('python manage.py test ' + ' '.join(result))


@task
def authors():
    '''Update the AUTHORS file.'''
    authors_path = join(env.huxley_root, 'AUTHORS')
    with hide('running'):
        local('git log --format="%%aN <%%aE>" | sort -u > %s' % authors_path)
        if local('git diff --name-only AUTHORS', capture=True):
            print green('Automatically updating the authors file...')
            local('git commit -m "Update AUTHORS." %s' % authors_path)
        else:
            print green('No change to AUTHORS.')


@task
def pr(number):
    '''Prepare and push a pull request.'''
    url = 'https://api.github.com/repos/bmun/huxley/pulls/%s' % number
    pr = json.loads(urllib2.urlopen(url).read())
    author = pr['head']['user']['login']
    repo = pr['head']['repo']['clone_url']
    branch = pr['head']['ref']

    print green('Checking out %s from %s...' % (branch, author))
    local('git fetch %s %s:%s' % (repo, branch, branch))
    local('git checkout %s' % branch)

    print green('Changes checked out. Rebasing and squashing...')
    local('git fetch origin; git rebase origin/master')
    commits_ahead = git.commits_ahead('origin')
    local('git rebase -i HEAD~%d' % commits_ahead)

    if not confirm(yellow('Changes squashed. Push?')):
        abort('Push canceled.')

    local('git checkout master; git merge %s --ff-only' % branch)
    local('git pull --rebase')
    local('git push')

    print green('Changes pushed! Deleting branch...')
    local('git branch -d %s' % branch)


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
def finish(branch_name=None, remote='origin'):
    '''Delete the current feature branch.'''
    prompt = yellow('This will delete your local and remote topic branches. '
                    'Make sure your pull request has been merged or closed. '
                    'Are you sure you want to finish this branch?')
    if not confirm(prompt):
        abort('Branch deletion canceled.')

    print green('Branch %s successfully cleaned up.' % git.cleanup(branch_name,
                                                                   remote))

try:
    from deploy import deploy
except ImportError:
    pass
