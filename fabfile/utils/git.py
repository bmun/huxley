# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from fabric.api import hide, local, settings
from fabric.colors import red

def master_guard(fn):
    def guarded_fn(*args, **kwargs):
        if current_branch() == 'master':
            print red('Currently on master branch. '
                      'You probably don\'t want to do this. Aborting.')
            return
        fn(*args, **kwargs)
    return guarded_fn

def new_branch(branch_name, remote='upstream'):
    local('git fetch %s' % remote)
    local('git checkout -tb %s %s/master' % (branch_name, remote))

def current_branch():
    with hide('running'):
        return local('git rev-parse --abbrev-ref HEAD', capture=True)

def remote_branch_exists(branch_name=None, remote='upstream'):
    branch_name = branch_name or current_branch()
    with hide('running'):
        heads_list = local('git ls-remote --heads %s' % remote, capture=True).split('\n')
    full_name = 'refs/heads/%s' % branch_name
    return any(full_name in head for head in heads_list)

def commits_ahead(remote='upstream'):
    with hide('running'):
        commit_list = local('git rev-list --left-right %s/master...HEAD' % remote, capture=True)
    return len(commit_list.split('\n'))

def pull(rebase=True):
    rebase_flag = '--rebase' if rebase else ''
    local('git pull %s' % rebase_flag)

def hub_installed():
    with hide('running', 'warnings', 'stdout', 'stderr'), settings(warn_only=True):
        return local('hub').return_code != 127

@master_guard
def push(branch_name=None):
    branch_name = branch_name or current_branch()
    local('git push origin %s --force' % branch_name)

@master_guard
def cleanup(branch_name=None, remote='upstream'):
    branch_name = branch_name or current_branch()

    if remote_branch_exists(branch_name, remote):
        print "Deleting remote branch..."
        local('git push origin :%s' % branch_name)

    print "Deleting local branch..."
    local('git checkout master')
    local('git branch -D %s' % branch_name)

    return branch_name
