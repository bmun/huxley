from fabric.api import run, local
from fabric.contrib.console import confirm

def feature(branch_name=''):
    if not branch_name:
        print "No branch name given. Usage: fab feature:<branch_name>"
        return
    local('git checkout -tb %s' % branch_name)

def update(remote='upstream'):
    local('git fetch %s' % remote);
    local('git rebase %s/master' % remote)

def review():
    print "Updating your current branch..."
    update()
    
    print "Pushing to remote topic branch..."
    branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)
    local('git push origin %s' % branch_name)
    
    print "Issuing pull request..."
    local('hub pull-request -b kmeht:master')

def finish():
    branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)
    if branch_name == 'master':
        print "On branch master. You probably don't want to do this."
        return
    
    if not confirm("This will delete your local and remote topic branch. "
                   "Make sure your pull request has been merged or closed. "
                   "Are you sure you want to finish this branch?"):
        print "Aborting."
        return

    print "Deleting remote branch..."
    local('git push origin :%s' % branch_name)

    print "Deleting local branch..."
    local('git checkout master')
    local('git branch -D %s' % branch_name)

