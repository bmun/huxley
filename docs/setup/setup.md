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
