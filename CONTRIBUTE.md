# Contribute to Huxley
We're really excited for you to start contributing to Huxley. Below are the detailed steps to get started and submit a patch.
NOTE: These instructions assume you're developing on Mac OS X. If you're on another platform, please consult the setup guides (coming soon!).

### Set Up Virtualenv and RVM
Virtualenv and RVM separate your project's Python and Ruby modules from the rest of your system to prevent conflicts.

### Create a Fork and Clone
Begin by creatig a fork of this repository. Go to the top-right of this repository page and click "Fork" (read Github's [guide](http://help.github.com/forking/) for a refresher on forking). Then, clone your repository:

	git clone https://yourusername@github.com/yourusername/huxley.git

### Install Dependencies
Install the Python dependencies as follows:

	pip install django
	pip install south
	pip install django-pipeline
	pip install yuicompressor

Then, create a Huxley gemset (it may already be created for you from the .rvmrc file) and install SASS:

	rvm use --create @huxley
	gem install sass

### Initial Setup
- Set up the database schema with `python manage.py syncdb`. Make a superuser if prompted.
- Then, update the migration history to reflect this with `python manage.py migrate --fake`.
- Compile static assets with `python manage.py collectstatic --noinput`.
- Run the server with `python manage.py runserver`. You'll now be able to access Huxley at localhost:8000.
- With that, you're ready to go; start hacking!
