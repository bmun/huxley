The purpose of this tutorial is to give you a sense of the basic architecture of Huxley and all its relevant components on a much smaller and easier to conceptualize scale. To do this we're going to walk through a tutorial of how to build a web application with a React JS front end and a Django back end.

##### Set up
This section will go over how to setup a django project. First create a directory somewhere in your file system called `huxleytutorial`. To do this open up your command prompt and type

```
$ mkdir huxleytutorial
$ cd huxleytutorial
```

Next we need to make sure you have python installed and django installed. To check if you have python installed run `python` on your command line. If you have python installed you should see something like this:

```
Python 2.7.10 (default, Oct 23 2015, 18:05:06)
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

If the command prompt doesn't show you this or says something like this:

```
-bash: python: command not found
```

Go download version 2.7 of python [here](https://www.python.org/downloads/).

After you've ensured you've downloaded python it's time to check to make sure you've downloaded django. To do that run `python` on your command line. Then do the following:

```
>>> import django
>>> print(django.get_version())
1.11
```

If you get an error or nothing prints. Download the latest version of Django [here](https://docs.djangoproject.com/en/1.11/intro/install/#install-django). It's easiest to install using pip, so make sure that you have pip installed/updated here: https://pip.pypa.io/en/stable/installing/#upgrading-pip
(You can test to make sure you have pip by running the "which pip" command from terminal).

Now that we've verified Python and Django are installed, let's create a django project. In your `huxleytutorial` directory run
```
$ django-admin.py startproject huxleytutorial
$ cd huxleytutorial
```

This creates a new django project for you. On top of this project we will build our app.

##### Loading html from the server
We're going to create a django application to hold our front end code. To create the app run this command in your huxleytutorial directory that has manage.py in it:

```
$ python manage.py startapp www
```
We call this app `www` for conventional reasons. Then move this app into your `huxleytutorial` directory.
```
$ mv www ./huxleytutorial
```
Your file structure should look like this:

```
huxleytutorial
    huxleytutorial
        www
        __init__.py
        settings.py
        urls.py
        wsgi.py
    manage.py
```

You will also need to add this app to your list of installed apps in settings.py. Go to settings.py and change the section titled INSTALLED_APPS to be

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'huxleytutorial.www',
)
```

Now let's begin creating our front end. To do this create a folder in your `www` directory called `templates`, and in that directory create a file called `www.html`. 
```
$ mkdir huxleytutorial/www/templates
$ touch huxleytutorial/www/templates/www.html
```

`www.html` will be the html backbone of our application. Your file structure should look like this now:
```
huxleytutorial
    huxleytutorial
        www
            templates
                www.html
            __init__.py
            views.py
        __init__.py
        settings.py
        urls.py
        wsgi.py
    manage.py
```

For now put this code in your `www.html` file:
```
<!DOCTYPE html>
<html lang="en-us">
<head>
    <title>Huxley Tutorial</title>
</head>
<body>
    <p>Hello, world!</p>
</body>
</html>
```
To see this web page open up chrome and in a new tab go to File>Open File and then find your `www.html` and open it. You should see your "Hello, world!" in the top left corner.

Let's now load this page from our server using a GET request. To do this place the following code in `huxleytutorial/urls.py`:

```
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('huxleytutorial.www.urls')),
)
```

Then create a file called `urls.py` in `huxleytutorial/www`:
```
touch huxleytutorial/www/urls.py
```
And place this code in there:
```
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'', views.index),
)
```
Then in `www/views.py` place the following code:
```
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'www.html')
```

Go to your command line and then run `python manage.py runserver`. Go to your browser and in your address bar open up `localhost:8000`. You should see your Hello, world! on the screen.

So what just happened. We created an html file that says hello world. Then whenever a browser sends a request with the URL '/' (or just an empty url) it routes it to our url in the www app and then routes the request to our view function index and index loads our html file into a response, and then sends the response back to the browser. When the browser gets the response it displays the html. That is how our front end connects to our back end.

##### Developing our front end/front end set up
We're now going to get our front end set up and start building on it. To do this create a directory in your www app called static. In the static folder create another folder called js. In your js folder create a file called app.js. app.js will be our front end entry point to our application.

In app.js place the following code
```
var React = require('react');

var TodoApp = require('./components/TodoApp');

React.render(
  <TodoApp />,
  document.getElementById('main')
);
```
Then in your js folder create another folder called components. In that folder create a file called TodoApp.js. In TodoApp.js place the following code
```
var React = require('react');

var TodoApp = React.createClass({
    render: function() {
        return (
            <p>Hello, world</p>
        );
    }
});

module.exports = TodoApp;
```

Then in www.html change the line `<p>Hello, world!</p>` to `<div id="main"></div>`

We are almost ready to load run our application. Ideally what we want is to run `python manage.py runserver` and see our Hello, world! at the top left corner like we did earlier. The difference now is that we're using React JS to do this. However there are a few things we need to do in order for this to work. In order to do those things we need to introduce npm. npm is a package manager and what it does is it will install packages onto your application that will allow certain things to run. For example we need to install a package to run react. We need to install a package to parse the JSX syntax of react. We also need to install a package to compile all our javascript code into a format that the browser can understand. The `require` keyword you see in the code is not something the browser can interpret and so we need a package to prepare our code to be interpreted by the browser.

The packages we are going to install to do all this are react, reactify, and browserify. To install them you must have `npm` and Node.js installed on your computer. To check if they're installed run `node -v` and `npm -v` on your command line. If something like `v0.10.40` and `1.4.28` is printed to your terminal for each respectively then they are installed. If not to install them you can use `brew` if you have it installed (this [article](http://blog.teamtreehouse.com/install-node-js-npm-mac) is helpful) or go to node's [website](https://nodejs.org/en/).

So go ahead and install them in your huxleytutorial directory that also has manage.py in it:
```
npm install react
npm install reactify
npm install browserify
```

If you don't have npm installed you should install. If you're running into errors try using `sudo npm install`.

So what do each of these do. `react` allows you to use react in your application. `reactify` parses the JSX syntax we're using to write our application. `browserify` looks for the word `require` starting out a particular file (in our case app.js) and then follows each `require` in each file that is required and bundles all of those files into one file that is eventually sent to the browser.

To get all this to work, in www.html, add the following line like so:
```
<!DOCTYPE html>
<html lang="en-us">
<head>
    <title>Huxley Tutorial</title>
</head>
<body>
    <div id="main"></div>
    <script src="../static/js/bundle.js"></script>
</body>
</html>
```

Then on your command line run the following command in your huxleytutorial directory that has manage.py in it:

```
browserify -t reactify ./huxleytutorial/www/static/js/app.js -o ./huxleytutorial/www/static/js/bundle.js
```
What this does is run browserify starting at app.js, parse through the JSX in each files, and puts them all in one file called bundle.js.

Now go and run `python manage.py runserver` and open up `localhost:8000`. You should see Hello, world! in the top left corner.

## Summary
What we've done here is demonstrated how to send a request from the browser to the server to load a webpage written in React. With this foundation you can now take what you've learned from the other tutorials to start building an appliation that uses React JS to interact with the user. A neat task would be to take to the ToDo app [tutorial](https://facebook.github.io/flux/docs/todo-list.html)using this set up. The front end code would be mostly the same as is provided in the tutorial. However now you have the challenge of reflecting data on the front end in your models in your django back end and synchronizing the todos you want saved, modified, and deleted on your front end with your backend by sending POST, PUT, and DELETE requests to your backend.
