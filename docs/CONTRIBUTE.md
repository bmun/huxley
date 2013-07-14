# Contribute to Huxley
We're really excited for you to start contributing to Huxley. Below are the detailed steps to help you get started. **If you're already set up, skip to [Submitting a Patch](https://github.com/kmeht/huxley/blob/master/docs/CONTRIBUTE.md#submitting-a-patch)!**

**NOTE**: These instructions assume you're developing on Mac OS X. If you're on another platform, please consult the setup guides (coming soon!).

## Getting Started

### Virtualenv
Virtualenv separates your project's Python modules from the rest of your system to prevent conflicts. We'll install virtualenv and a useful utility built on top of it, virtualenvwrapper.

	$ sudo pip install virtualenv
	$ sudo pip install virtualenvwrapper

Add the following two lines to your `.bash_profile` and source it:

	export WORKON_HOME="$HOME/.virtualenvs"
	source /usr/local/bin/virtualenvwrapper.sh

	# And in terminal:
	$ source ~/.bash_profile

You'll then be able to create a virtualenv for Huxley:

	$ mkvirtualenv huxley

From now on, whenever you're going to work on Huxley, just remember to switch to your `huxley` virtualenv (and deactivate it when you're done):

	$ workon huxley # When you're about to begin work
	...hack...
	$ deactivate # After you're done

### Hub
Hub is a command line interface to GitHub. Install it using Homebrew, with

	$ brew install hub

### Create a Fork and Clone
Begin by creating a fork of this repository. Go to the top-right of this repository page and click "Fork" (read Github's [guide](http://help.github.com/forking/) for a refresher on forking. If you're new to GitHub, remember to [set up SSH keys](https://help.github.com/articles/generating-ssh-keys) as well). Then, clone your repository, `cd` into it, and add this one as an upstream remote:

	$ git clone git@github.com:yourusername/huxley.git
	$ cd huxley
	$ git remote add upstream https://github.com/kmeht/huxley.git

### Install Dependencies
Install the Python dependencies with the provided `requirements.txt` (remember to activate the `huxley` virtualenv!):

	$ pip install -r requirements.txt

### Initial Setup
The first is to prepare the database. Huxley uses South, a schema migration management tool for Django. We'll generate our database
tables from the models, bring South's migration history up to speed, and load some test data:

	$ python manage.py syncdb # Make a superuser if prompted.
	$ python manage.py migrate --fake
	$ python manage.py loaddata countries committees advisor chair

We use Pipeline to collect, compile, and compress our static assets. It simply hooks into Django's `collectstatic` management command:

	$ python manage.py collectstatic --noinput

Lastly, spin up a development server so you can access Huxley at `localhost:8000`:

	$ python manage.py runserver

With that, you're ready to go; start hacking!


## Submitting a Patch
1. Create a new topic branch. Make the name short and descriptive: `fab feature:my-branch-name`.
2. Make your changes! Feel free to commit often.
3. Update your topic branch with `fab update`.
4. Request code review of your changes with `fab submit`.
5. Make changes and resubmit your code with `fab revise`.
5. After your pull request has been merged or closed, clean up your branches with `fab finish`.

### Tips
- **Use one topic branch per feature!** This will allow you to better track where your various changes are, and will make it easier for us to merge features into the main repository.
- **Follow style guidelines!** Make sure you've read the code style guidelines before making your changes.
- **Test your code!** If you add new functions, be sure to write unit tests for them, and modify existing unit tests already.
- **Update the documentation!** If you feel that your change warrants a change to the current documentation, please do update the documentation as well.
