# Huxley Integrated Tutorial
 
 
By this point you should feel familiar with the general structure of Huxley; the basics of Django and React and an idea of how the rest API bridges them together. This tutorial brings that knowledge into focus. You will be working on a full production-worthy feature that exercises the full code stack. Some of this tutorial will be guided, some of it will be open ended. The purpose is by the end for you to feel comfortable with adding code to Huxley.
 
What you will be adding is an interface for managing committee rooms. This will involve matching committees to rooms, handling seat assignments, adding room feedback, and more.
 
Make sure to checkout the learn branch from Huxley in git; this is where you will do all of your coding for this tutorial.

If at any point you feel confused, try a Google search. Knowing how to use Google when you're stuck is a useful skill to develop and usually the answer you're looking for can be found in documentation or on StackOverflow. Don't be afraid to reach out to any older Tech members as well! We are here to help you and know what it feels like to be just getting started. No matter how silly the question seems in your head, chances are one of us got stuck on it too at some point.


## Stop! Before doing anything else:
Go to `docs/setup.md` and run all the setup stuff there! Once everything works, run the following command in your Huxley directory to get the tutorial locally: `git checkout learn`. 

 
## Part 1: The Backend
 
This part will focus on adding the backend infrastructure to track the necessary information. This should be the first step you code when adding any new features; it would usually be preceded only by the design planning. For the purposes of this tutorial however, most of the design decisions have already been made for you.
 
#### Step 1
 
Open ```huxley/core/models.py```. (If you’re hoping for a list of beautiful humans you’ll be disappointed; these are models for how information is stored. For beautiful humans find a list of Tech Seniors). This file is something you will almost always edit when adding new functionality; the classes here you can think of as describing “things”: schools, committees, delegates, etc.  These describe all the information a type of thing could have, like a name, and control how the database stores the information.
 
Now find the ```Room``` class at the bottom of the file. You’ll notice that there’s an initial skeleton already in place; follow the instructions there.
 
#### Step 2
 
Now you will give the committee model a room. Scroll up to where the ```Committee``` class is defined. Here comes your first design decision! Don’t worry, it will only hurt a little bit.
 
When you’re relating two models you generally have three choice: one-to-one, many-to-many, and many-to-one. These are what they sound like. A one-to-one relation means that the two models only relate to each other. For example, if a committee has a rubric, then it has only that one rubric and no other committee has that rubric. Many-to-many means both models can be related to as many of each other as you want. For example, a committee can relate to many different countries and a country can relate to many different committees. And many-to-one (which is a ```ForeignKey``` field in Django) means that many different instances of a model can share the same relation to another model, but each of them can only relate to a single instance. For example, delegates have committees. Each delegate can only be in one committee, but a committee can have many delegates. These relations are all from the point of view of the class on which you define the relation (where you type the code).

Also, you have to decide what happens when the thing you're referencing is deleted! Every model relation takes in an `on_delete` argument; this can be set to either `models.CASCADE` or `models.SET_NULL`. In this case, we're using `models.SET_NULL` -- if a room disappears (maybe another club booked it!), we want to set our current room value to null instead of deleting our committee as a whole! However, there may be cases when we want to cascade that deletion downwards. For example, if a committee disappears, we want its assignment to disappear as well!
 
Now decide the best definition for a committee’s relation to a room.
 
Consider this:
 
* On any given day, a room can only be used by one committee
* Committees can move rooms between days
* The definition defines three rooms for a committee; one for each day
* A committee can move into a room another committee was using previously
* A committee can only ever be in one room 
* Head chairs are territorial and get anxious when you invade their space
* We don’t want head chairs to start biting people
 
The choice here will affect how you build out the code.
 
#### Step 3
 
So now there are rooms, and each committee has one for each day. Now we’ll give delegates seat assignments! Because we want power. Raw, untamed power. The power to command where people go. Like I have over you right now; go to the ```Delegate``` class. 
 
You’ll find several options for giving seat numbers here; select the one that is most appropriate. 
 
Consider this:
 
* A delegate only has a single seat number (so how will it work for each day?)
* The largest committee might have ~300 seats (a relatively smallinteger)
* You want a way to distinguish between delegates with assigned seats and those without; hint: perhaps use a special default value to represent unassigned?
 
Now we want to make sure two delegates don’t end up sitting on top of each other (they might want it, but we’d probably get sued so we’re going to disallow it). Look at ```Meta``` within the ```Delegate``` class. The ```Meta``` class defines rules the database uses to store the model. One such is the ```unique_together``` attribute; this means that only a single instance of the model can have a specific pairing of field values. In this case, no two delegates should have the same seat assignment in the same committee. But, this should only apply if a delegate actually has an assigned seat! You’re going to have to override a method called ```validate_unique``` in order to let two delegates in the same committee have the value for an unassigned seat. This is an example of a great time to Google something: we have a behavior (making it impossible for two delegates ot share a commitee and seat assignment) that almost does what we want, but it does not quite handle a use case we want (having an exception if the seat value matches the unassigned seat value).
 
#### Step 4
 
We’re almost finished with our models, but we’d still like to be able to leave comments on room. What if you found some left a live raccoon there overnight, and it had claimed the room for its DeCal on the benefits of open air trash cans? By golly you’d want to leave some biting critiques for the people who were supposed to make sure all rodents had vacated the prior evening!
 
This model you’ll going to define from scratch.
A ```RoomComment``` must have:

* A Room (a room can have many comments; this sounds like a …?)
* A Comment that is a TextField
* An integer rating that goes from one (the raccoon’s DeCal disrespects your political opinions on the subject) to ten (why I’d hardly believe they keep raccoons here when students aren’t around!)
 
You will also have to add the ```__str__``` method and the Metaclass; refer to other classes for examples on how to do this.
 
#### Step 5
 
Now that all this code exists, how can we start using it? We’re still far away from coding on the frontend. But we have an admin console that lets us manage things right? In a terminal, go to your Huxley folder and run: ```python manage.py runserver```
 
Log in to the admin panel (http://127.0.0.1:8000/admin/) and poke around. Hey, this looks like all the folders and code you were just looking at! You’ll see a lot of models here, but where are yours? Why aren’t they here? Are you telling me you just had me log in and you knew they wouldn’t even be here? What kind of sick freak are you?
 
There’s a file you have to edit to get your new code to pop up here. Open ```huxley/models/admin/__init__.py``` and fill in the code. Now go back to your web browser and refresh the page. See? There’s your stuff! That’s something you made.

One more thing you'll need to do before you finish and before you can start creating rooms: migrate!

In order to create database tables for your new models and modify ones for the models you modified, you need to run two commands: ```python3 manage.py makemigrations``` and ```python3 manage.py migrate```.

The former will create a list of changes to make to your database in the form of SQL queries, and the latter will update your database.

Now, you should be able to create new rooms!
 
#### Step 6
 
Play around with the admin panel. Sign up as an advisor, then add committees and delegates and see how you can give them rooms and assign seats. 
 
#### Step 7
 
The final thing to do is the test cases. (Ignore the chill that just went down your spine.)
 
Every directory in Huxley has an associated test folder that corresponds to the files in the directory. Find the folder ```huxley/core/tests``` and open up ```test_models.py```. For the unit tests here, we use Django ‘s built-in testing framework. 
 
A unit test should verify the smallest possible behavior of your code, hence the name “unit”. The idea is that the unit tests will provide detailed verification of your code, so if something breaks later on you can trace it back to the source.
 
We’ll start with ```RoomTest```. Go to the bottom of the file and you’ll see the skeleton mostly filled in. Follow the instructions there to finish the rest of it. Hint: for the ```__str__``` method, your answer will look something like ```self.room.field_name + “_” + self.room.field_name```.
 
Now find ```DelegateTest``` and fill in ```test_unique```.
 
Now the fun part. At the very bottom is ```RoomCommentTest```. And it has very bare-bones skeleton code (get it? get it?). Your job is to fill this in without any extra guidance, but you should mostly be doing what you did above. Think through what each method is trying to accomplish based off what you saw in other tests.
 
Now go to a terminal and from your Huxley directory type:
 
```
python manage.py test huxley.core.test.test_models
```
 
Did anything break? If so, it sounds like you need to fix your code! Make sure the unit test is correct first, and, if it is, find the place in models.py the test corresponds to. Note: DO NOT change the unit test until you pass it. Only change the unit test if there is a problem with the test itself. No taking the easy way out here.

There are plenty more tests we could add if we wanted to; unit tests always involve design decisions on what to include and what not to. It comes down to one question: what's going to be the most confusing later on if it breaks? It does not come down to: "writing unit tests is so boring please make it stop if you have any pity on my soul!" (I guarantee you will say almost these exact words at least a few hundred times in your coding career). Unit tests may be boring to do, but they are the backbone of any major codebase and you will be glad you wrote them.
 
#### Step 8
 
Commit your code changes and push them to your local repository now, if you haven’t been doing that already. (You should do this as often as possible. Feel shame now. Deep shame. You forgot to commit, didn’t you? And what is life without commitment?).

Remember, you can commit using the following series of commands:

```
git add [files and/or directories you want to commit, separated by spaces]
git commit -m "commit message here"
```

## Part 2: The Frontend

Now that we've added things to the backend, we can start thinking about what people will see! Where might we use this information in Huxley? Remember, Huxley has three kinds of users: the delegate, the advisor, and the chair.

We can use our newly-created rooms to provide information to two of these groups!
* Advisors want to know what rooms their delegates are in so they can see how they're doing.
* Chairs want to know what seat numbers each of their delegates is in so they can easily keep track of what's happening in the room.

Before we get started, try "registering" for BMUN (on your local server -- http://127.0.0.1:8000/ -- not the actual Huxley website) and creating a fake advisor account with some delegates! Also create a fake chair account by going to the admin panel (/admin) and going to "Users". 

#### Step 1
In order to have data available on the frontend for the second part of this tutorial, you'll first need to create ways for the data to be passed to the frontend! This is done through the Huxley API, which is defined in `huxley/api`. In order to pass our new data data to our frontend, we'll need to create a serializer for each model we've created and modify the serializers for our Committee and Delegate models.

1. To start, we can make a simple change to the Delegate model -- the only field we added there was `seat_number`. Add `'seat_number'` to the `fields` attribute of the `Meta` class of the `DelegateSerializer` class in `api/serializers/delegate.py` (that's a lot of "of"s!).

2. Next, we'll need to change the `CommitteeSerializer` class in `api/serializers/committee.py`. We want to add our `room_day_one`, `room_day_two`, and `room_day_three` attributes the same way we did for the delegate serializer. However, you might notice that these aren't just attributes -- they also refer to other models! By default, the data passed through these will be their ids. In order to pass all of the room data up instead of just their ids, we'll need to pass in a `RoomSerializer` for each `room_day_xxx` field. Mimic at what has been done for `Rubric` in the `CommitteeSerializer` class for each day's room.

3. Let's create our `RoomSerializer`! In `room.py`, update the `RoomSerializer` class to contain a `Meta` class with `fields` that are the attributes you want to pass to the frontend. For reference, you may want to look at `rubric.py`.

**Note: at this point in time, you would ordinarily also need to modify the `test_committee.py` and `test_delegate.py` files, but for time, we'll skip that for now!**

#### Step 2

The very first thing we're going to do in JavaScript is add an extra column to the advisors' assignments table containing delegates' rooms. This is located in `AdvisorAssignmentsView.js`. To change what the advisor sees, we will be modifying the `render` function! We'll be adding three extra columns. Try filling in the `TODO` comments with code that will add delegates' seats on days 1, 2, and 3 to the advisors' tables!

You will want three columns to your table: one for each column.

There are a few things you will need to do here:
- Update the table column names
- Update each column values to pull data from the backend

When working with tables, note that the `tr` tag in HTML denotes a row, and the `td` tag denotes a cell within that row. 

Hint: You can get a `committee` object for a given assignment by using `committees[assignment.committee]`; this will have the same fields as the corresponding committee object in `models.py`.

Once you have this code, you can see if your code works by running `npm run build` in a new terminal tab, opening up Huxley, and logging in as an advisor! You may want to run your browser in incognito to make sure any changes load and haven't been cached.

#### Step 3

Now, add three columns to `ChairDelegateEmailView.js` so that chairs are able to see where their delegates are seated on each day! In this case, you should be using seat numbers for each delegate.

There are no `TODO` comments here -- try seeing how the code is similar to the previous file you edited!

Hint: How does the rest of the code get a specific assignment? What about a delegate? What field holds a delegate's seat number, and what object is it located in?

Once you have this code, you can see if your code works by running `npm run build` in a new terminal tab, opening up Huxley, and logging in as an chair! You may want to run your browser in incognito to make sure any changes load and haven't been cached.

#### Step 4

Congratulations, you've finished your tutorial! Of course, you have to make sure to test your code -- to do so, run the test server using `python manage.py runserver` and then log into the fake advisor account / fake chair accounts you created! Head's up: you might need to create some fake delegates as well so you can assign them seat numbers.

Commit and push your code, and let your Tech know that you're done!