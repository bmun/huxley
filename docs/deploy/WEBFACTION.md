## WebFaction Deployment Guide
BMUN's Web host of choice is WebFaction, due to their commitment to hosting the latest version of popular software, numerous one-click install options, and customizable server configuration. If you're deploying on another host, please contribute a guide!

**Guide last updated: 08/25/2014.** If you run into issues with this guide, try [WebFaction's own Django deployment guide!](http://docs.webfaction.com/software/django/getting-started.html) (And of course, [open an issue](https://github.com/bmun/huxley/issues) so we can improve ours :)

### First steps
Before we get started, you'll need to have a WebFaction account. Then, using WebFaction's one-click installer, install the latest version of Django/Python. Lastly, create a static files application for your app using [Webfaction's guide](http://docs.webfaction.com/software/django/getting-started.html#create-a-website-with-django-and-static-media-applications). We assume that you have `ssh` access to your server as well. **All steps in this guide happen on your WebFactionServer.**

We'll also alias the latest version of Python to the `python` command. Add the following lines to your `.bashrc` file.

```sh
export PYTHONVER=2.7
export PYTHON=python${PYTHONVER}

alias python=${PYTHON}
```

Source your `.bashrc` file with:

```sh
$ source ~/.bashrc
```

### Get the Code
Once you've created an empty Django app, the one-click installer creates a new directory in your `~/webapps` directory named huxley. The default Django code is located in `~/webapps/huxley/myproject`. We're gonna get rid of that and clone our repo:

```sh
$ cd ~/webapps/huxley
$ rm -rf myproject
$ git clone <your huxley fork>
```

We'll need to tell the server to look for our code there. Open the file `~/webapps/huxley/apache2/conf/httpd.conf`. Find the following two lines, and replace "myproject" with "huxley":

```
WSGIDaemonProcess huxley processes=2 threads=12 python-path=/home/bmun/webapps/huxley:/home/bmun/webapps/huxley/myproject:/home/bmun/webapps/huxley/lib/python2.7
WSGIScriptAlias / /home/bmun/webapps/huxley/myproject/myproject/wsgi.py
```

Lastly, we want to use the Django from our virtualenv. Webfaction's Python setup prioritizes modules installed in the app's `lib` directory over modules in the virtualenv (more info [here](http://docs.webfaction.com/software/python.html#python-search-path)), which means we'll actually be removing the Django installed by the one-click installer!

```sh
$ rm -r ~/webapps/huxley/lib/python2.7/django
```

### Virtualenv
Just like during development, we need a virtualenv. As of this writing, WebFaction doesn't have pip installed, so we have to install it along with virtualenv and virtualenvwrapper:

```sh
$ easy_install-${PYTHONVER} pip
$ pip install virtualenv
$ pip install virtualenvwrapper
```

We then have to add some configuration for virtualenvwrapper to function properly. First, make a directory for your virtualenvs:

```sh
$ mkdir ~/.virtualenvs
```

Then, add the following lines to your `.bashrc` and source it again:

```sh
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_TMPDIR=$HOME/.virtualenvs/tmp
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/$PYTHON
source $HOME/bin/virtualenvwrapper.sh
```

Finally, let's create our virtualenv and install the necessary packages:

```sh
$ cd ~/webapps/huxley/huxley
$ mkvirtualenv huxley
...huxley virtualenv created...
...pip installed...
(huxley)$ pip install -r requirements.txt
```

If you'll be using MySQL, there's one more package we'll need to install:

```sh
(huxley)$ pip install MySQL-python
```

### Install Node/NPM
Huxley's JavaScript code is organized as node modules and packaged for the browser with Browserify. Webfaction provides one-click installers for Node apps, but since this is just using it as part of a build step, a global install is easier to deal with.

To install it, follow the directions under the **Install Node.js** section of [this StackOverflow answer](http://stackoverflow.com/a/18687851). After that, you can install JS dependencies with `npm`:

```sh
$ cd ~/webapps/huxley/huxley
$ npm install
```

### Create a Database
Follow WebFaction's instructions to create a MySQL or PostgreSQL database, and write down the password. That's it for the database step :)

### Configure the Application

First, let's configure our deployment settings by specifying a local settings file. Copy the `local.py.default` file in the `huxley/settings` directory:

```sh
$ cd ~/webapps/huxley/huxley/huxley/settings
$ cp local.py.default local.py
```

Then, open `local.py` in your editor of choice and fill out the settings.

Finally, you'll need a `wsgi.py` file. We've provided a default one, so copy it and slightly modify it to add your virtualenv to its python path:

```sh
$ cd ~/webapps/huxley/huxley
$ cp wsgi.py.default wsgi.py
```

And, in `wsgi.py`:

```python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'huxley.settings'

# Add the following two lines:
activate_this = os.path.expanduser("~/.virtualenvs/huxley/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
```

### Sync Database
Finally, prepare your database and restart the application. Remember to activate your virtualenv!

```sh
$ cd ~/webapps/huxley/huxley
$ workon huxley
(huxley)$ python manage.py syncdb
(huxley)$ python manage.py migrate
(huxley)$ python manage.py collectstatic --noinput # Not really database-related, but whatever.
(huxley)$ ~/webapps/huxley/apache2/bin/restart # Restart the server process
```

### Mount the Application
In your WebFaction control panel, create a new website, and mount your Huxley application at the root URL. Mount the static application you created on the /static URL. You may have to wait a few minutes for the changes to take effect. Then, visit www.yourdomain.com to see Huxley up and running!
