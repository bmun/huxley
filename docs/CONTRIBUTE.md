# Contribute to Huxley
We're really excited for you to start contributing to Huxley. Below are the detailed steps to get started and submit a patch.
NOTE: These instructions assume you're developing on Mac OS X. If you're on another platform, please consult the setup guides (coming soon!).


## Getting Started

### Virtualenv and RVM
Virtualenv and RVM separate your project's Python and Ruby modules from the rest of your system to prevent conflicts.

First, we'll start out with virtualenv (and a useful utility built on top of it, virtualenvwrapper).

	$ sudo pip install virtualenv
	$ sudo pip install virtualenvwrapper

Add the following two lines to your `.bash_profile` and source it:

	export WORKON_HOME="$HOME/.virtualenvs"
	source /usr/local/bin/virtualenvwrapper.sh

	# And in terminal:
	$ source ~/.bash_profile

You'll then be able to create a virtualenv for Huxley:

	$ mkvirtualenv huxley

From now on, whenever you're going to work on Huxley, just remember to switch to your `huxley` virtualenv:

	# When you're about to begin work
	$ workon huxley
	
	# After you're done
	$ deactivate


### Create a Fork and Clone
Begin by creating a fork of this repository. Go to the top-right of this repository page and click "Fork" (read Github's [guide](http://help.github.com/forking/) for a refresher on forking). Then, clone your repository:

	git clone git@github.com/yourusername/huxley.git

### Install Dependencies
Install the Python dependencies as follows:

	pip install django
	pip install south
	pip install django-pipeline
	pip install coverage
	pip install yuicompressor

Then, create a Huxley gemset (it may already be created for you from the .rvmrc file) and install SASS:

	rvm use --create @huxley
	gem install sass

### Initial Setup
The first is to prepare the database. Huxley uses South, a schema migration management tool for Django. We'll generate our database
tables from the models, bring South's migration history up to speed, and load some test data:

	python manage.py syncdb # Make a superuser if prompted.
	python manage.py migrate --fake
	python manage.py loaddata countries committees

We use Pipeline to collect, compile, and compress our static assets. It simply hooks into Django's `collectstatic` management command:

	python manage.py collectstatic --noinput

Lastly, spin up a development server so you can access Huxley at `localhost:8000`:

	python manage.py runserver

With that, you're ready to go; start hacking!


## Submitting a Patch