# Contribute to Huxley
We're really excited for you to start contributing to Huxley. Below are the detailed steps to get started and submit a patch.
NOTE: These instructions assume you're developing on Mac OS X. If you're on another platform, please consult the setup guides (coming soon!).


## Getting Started

### Virtualenv and RVM
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
The first is to prepare the database. Huxley uses South, a schema migrationm management tool for Django. We'll generate our database
tables from the models, and bring South's migration history up to speed:

	python manage.py syncdb # Make a superuser if prompted.
	python manage.py migrate --fake

We use Pipeline to collect, compile, and compress our static assets. It simply hooks into Django's `collectstatic` management command:

	python manage.py collectstatic --noinput

Lastly, spin up a development server so you can access Huxley at `localhost:8000`:

	python manage.py runserver

With that, you're ready to go; start hacking!


## Submitting a Patch