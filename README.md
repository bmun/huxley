# Huxley
Huxley is a web application designed to manage the annual [Berkeley Model United Nations](http://bmun.org/) conference.

## About BMUN
The Berkeley Model United Nations conference is a high-school conference hosted every spring. Each year, we host over 1500 delegates from all over the country (and the world!), who compete in a simulation of the United Nations (as well as other international and historical bodies) to solve the world's most compelling problems.


## About Huxley
Huxley was initially conceived as a way to abstract away database access from club officers in order to maintain consistency of the data. As the size of our conference grew, so did the logistical complexity, prompting us to begin developing a web application to centralize our data and streamline its access. 

Huxley's built with [Django](http://www.djangoproject.com), a web development framework written in [Python](http://www.python.org). The frontend is simple HTML and CSS, and makes heavy use of [jQuery](http://jquery.com/).

## Contribute
We'd love for you to contribute to Huxley! Here's some stuff you'll find useful:

### Dependencies
Huxley is built with Django, a web development framework written in Python. It additionally has the following dependencies:
- [South](http://south.aeracode.org): A Django utility for managing schema migrations
- [Pipeline](http://django-pipeline.readthedocs.org/en/latest): A Django utility for managing and compressing static files
- [YUI Compressor](http://yui.github.com/yuicompressor/): A utility used for compressing JavaScript and CSS files

### Getting Started
Note: Before proceeding, remember to set up a Python [virtualenv](http://www.virtualenv.org/en/latest/), to separate your packages from the rest of your system.


**Install Django and Dependencies**

Installing these packages is as simple as

	pip install django
	pip install south
	pip install django-pipeline

To install the YUI Compressor, download a binary and place it somewhere on your PATH.


**Create a Fork and Clone the Repo**

Create a fork of this repository by going to <https://github.com/kmeht/huxley/fork> (read Github's [guide](http://help.github.com/forking/) for a refresher on forking). Then, clone the repository with `git clone https://yourusername@github.com/yourusername/huxley.git`.


**Initial Setup**


**Submitting a Patch**


### BSD License
Copyright (c) 2011-2013, Kunal Mehta.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
