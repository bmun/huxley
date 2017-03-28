# Ubuntu Setup

This guide details the steps to set up Huxley on Ubuntu. Use this if you'd like to customize your setup, or had trouble with the setup script.

### Pip
Pip allows you to install python packages that will help you develop python applications.
	
    $ sudo apt-get update 
    # updates your repository so you can get the newest version of the package

    $ sudo apt-get install python-pip

### Virtualenv
Virtualenv separates your project's Python modules from the rest of your system to prevent conflicts. We'll install virtualenv and a useful utility built on top of it, virtualenvwrapper.

    $ sudo pip install virtualenv
    $ sudo pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs
	
    $ which python
    # Make sure this refers to the correct python package on your computer
    # Most likely "/usr/bin/python"

Open "~/.bashrc" with a text editor and add the lines

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper/virtualenvwrapper.sh
    # This may not necessarily be the path to your virtualenvwrapper.sh, confirm that it is there first

    # In terminal
    $ source ~/.bashrc

    # Or exit Terminal and reopen it
	
You'll then be able to create a virtualenv for Huxley:

    $ mkvirtualenv huxley

From now on, whenever you're going to work on Huxley, just remember to switch to your `huxley` virtualenv (and deactivate it when you're done):

    $ workon huxley # When you're about to begin work
    ...hack...
    $ deactivate # After you're done

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

    $ sudo pip install -r requirements.txt
    
Install the JS dependencies with the provided `package.json` using npm:

    $ sudo apt-get install npm
    $ sudo npm install

### Initial Setup
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
