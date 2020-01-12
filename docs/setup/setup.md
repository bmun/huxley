# Setup
This guide details setup instructions for Huxley.

### venv
Virtual environments create isolated places to install packages -- if one project you're working on requires version 1.0 and another requires version 2.0, you can't have both at once! However, using a virtual environment, you can, as you have separate "environments," each with its own Python installation.

Python3 comes bundled with a module that allows you to create virtual environments.

To create a virtual environment, navigate to `huxley/env` and run the following commands:
```
$ python3 -m venv huxley
```
This will create a virtual environment located in the `env` directory in huxley.

Then, all you need to do is activate it!

On Windows, this is done by running:
```
$ env\huxley\Scripts\activate.bat
```
from the main Huxley directory.

On Mac or Linux, you can run:
```
source env/huxley/bin/activate
```

Your virtual environment will now be activated. Things you do inside your virtual environment stay inside your virtual environment!

To deactivate, all you need to do is type `deactivate` into the command line.

### Create a Fork and Clone
Begin by creating a fork of this repository. Go to the top-right of this repository page and click "Fork" (read Github's [guide](http://help.github.com/forking/) for a refresher on forking. If you're new to GitHub, remember to [set up SSH keys](https://help.github.com/articles/generating-ssh-keys) as well). Then, clone your repository, `cd` into it, and add this one as an upstream remote:

    $ git clone git@github.com:yourusername/huxley.git
    $ cd huxley
    $ git remote add upstream https://github.com/kmeht/huxley.git

Next, configure your author information. Use your name and email as they appear on GitHub:

    $ git config user.name "Your Name"
    $ git config user.email "your@github.email"

### Install Dependencies
Install the Python dependencies with the provided `requirements.txt` (remember to activate the `huxley` virtualenv!):

    $ pip install -r requirements.txt
    
Install the JS dependencies with the provided `package.json` using npm:

    $ npm install

Setup
The first step is to prepare the database. We do that by running: 

    $ python manage.py runserver

Running the server will automatically create a database for us at `huxley/huxley.db`. Once you've run the server exit it (CONTROL-C), and then run:

    $ python manage.py migrate
    $ python manage.py loaddata conference countries committees advisor chair

Finally, we use Pipeline to collect, compile, and compress our static assets. It simply hooks into Django's `collectstatic` management command:

    $ python manage.py collectstatic --noinput
    
If you run into an error here run `ulimit -n 512`. This will increase the number of files the process running Huxley will be allowed to open.

Next, you need to compile your JS code by running:

    $ npm run build

Lastly, open up a new tab in your terminal (make sure you're still in your virtualenv), and spin up a development server:

    $ python manage.py runserver

You can access Huxley at `localhost:8000`.


If you haven't created a superuser yet, you should do that now:

    $ python manage.py createsuperuser
    
Your superuser credentials is what will allow you to login to the admin panel at `localhost:8000/admin/`.

To check out the other management commands at your disposal run `python manage.py`. This will list out all possible management commands. Many of these commands will be useful to keep your development environment in check.

With that, you're ready to go; start hacking!
