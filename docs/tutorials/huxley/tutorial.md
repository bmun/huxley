# Huxley Integrated Tutorial
 
 
By this point you should feel familiar with the general structure of Huxley; the basics of Django and React and an idea of how the rest API bridges them together. This tutorial brings that knowledge into focus. You will be working on a full production-worthy feature that exercises the full code stack. Some of this tutorial will be guided, some of it will be open ended. The purpose is by the end for you to feel comfortable with adding code to Huxley.
 
What you will be adding is an interface for managing committee rooms. This will involve matching committees to rooms, handling seat assignments, adding room feedback, and more.
 
Quick note: it’s important to clarify terminology. An instance refers to a specific thing, while a model/class is a general type. For example, Jake is an instance of the Human class (supposedly). 
 
Make sure to checkout the learn branch from Huxley in git; this is where you will do all of your coding for this tutorial.
 
 
## Part 1: The Backend
 
This part will focus on adding the backend infrastructure to track the necessary information and expose the necessary endpoints for the REST api.
 
#### Step 1
 
Open ```huxley/core/models.py```. (If you’re hoping for a list of beautiful humans you’ll be disappointed; these are models for how information is stored. For beautiful humans find a list of Tech Seniors). This file is something you will almost always edit when adding new functionality; the classes here you can think of as describing “things”: schools, committees, delegates, etc.  These describe all the information a type of thing could have, like a name, and control how the database stores the information.
 
Now find the ```Room``` class at the bottom of the file. You’ll notice that there’s an initial skeleton already in place; follow the instructions there.
 
#### Step 2
 
Now you will give the committee model a room. Scroll up to where the ```Committee``` class is defined. Here comes your first design decision! Don’t worry, it will only hurt a little bit.
 
When you’re relating two models you generally have three choice: one-to-one, many-to-many, and many-to-one. These are what they sound like. A one-to-one key means that the two models only relate to each other. For example, if a committee has a rubric then it has only that rubric and no other committee has that rubric. Many-to-many means both models can be related to as many of each other as you want. For example, a committee can relate to many different countries and a country can relate to many different committees. And many-to-one (which is a ```ForeignKey``` field in Django) means that many different instances of a model can share the same relation to another model, but each of them can only relate to a single instance. For example, delegates have committees. Each delegate can only be in one committee, but a committee can have many delegates. These relations are all from the point of view of the class on which you define the relation (where you type the code).
 
Now decide the best definition for a committee’s relation to a room.
 
Consider this:
 
*     On any given day, a room can only be used by one committee
*     Committees can move rooms between days
*     The definition defines three rooms for a committee; one for each day
*     A committee can move into a room another committee was using previously
*     A committee can only ever be in one room 
*     Head chairs are territorial and get anxious when you invade their space
*     We don’t want head chairs to start biting people (most people)
 
The choice here will affect how you build out the code.
 
#### Step 3
 
So now there are rooms, and each committee has one for each day. Now we’ll give delegates seat assignments! Because we want power. Raw, untamed power. The power to command where people go. Like I have over you right now; go to the ```Delegate``` class. 
 
You’ll find several options for giving seat numbers here; select the one that is most appropriate. 
 
Consider this:
 
*     A delegate only has a single seat number (so how will it work for each day?)
*     The largest committee might have ~300 seats (a relatively smallinteger)
*     You want a way to distinguish between delegates with assigned seats and those without; hint: perhaps use a special default value to represent unassigned?
 
Now we want to make sure two delegates don’t end up sitting on top of each other (they might want it, but we’d probably get sued so we’re going to disallow it). Look at ```Meta``` within the ```Delegate``` class. The ```Meta``` class defines rules the database uses to store the model. One such is the ```unique_together``` attribute; this means that only a single instance of the model can have a specific pairing. But, this should only apply if the delegate actually has an assigned seat! You’re going to have to override a method called ```validate_unique```.
 
#### Step 4
 
We’re almost finished with our models, but we’d still like to be able to leave comments on room. What if you found some left a live raccoon there overnight, and it had claimed the room for its DeCal on the benefits of open air trash cans? By golly you’d want to leave some biting critiques for the people who were supposed to make sure all rodents had vacated the prior evening!
 
This model you’ll going to define from scratch.
A ```RoomComment``` must have:

*  A Room (a room can have many comments; this sounds like a …?)
*     A Comment that is a TextField
*     An integer rating that goes from one (the raccoon’s DeCal disrespects your political opinions on the subject) to ten (why I’d hardly believe they keep raccoons here when students aren’t around!)
 
You will also have to add the Unicode method and the Metaclass; refer to other classes for examples on how to do this.
 
#### Step 5
 
Now that all this code exists, how can we start using it? We’re still far away from coding on the frontend. But we have an admin console that lets us manage things right? In a terminal, go to your Huxley folder and run: ```python manage.py runserver```
 
Log in to the admin panel (http://127.0.0.1:8000/admin/) and poke around. Hey, this looks like all the folders and code you were just looking at! You’ll see a lot of models here, but where are yours? Why aren’t they here? Are you telling me you just had me log in and you knew they wouldn’t even be here? What kind of sick freak are you?
 
There’s a file you have to edit to get your new code to pop up here. Open ```huxley/models/admin/__init__.py``` and fill in the code. Now go back to your web browser and refresh the page. See? There’s your stuff! That’s something you made.
 
#### Step 6
 
Play around with the admin panel. Add committees and delegates and whatnot, see how you can give them rooms and assign seats.
 
#### Step 7
 
The final thing to do is the test cases. (Ignore the chill that just went down your spine.)
 
Every directory in Huxley has an associated test folder that corresponds to the files in the directory. Find the folder ```huxley/core/tests``` and open up ```test_models.py```. For the unit tests here, we use Django ‘s built-in testing framework. 
 
A unit test should verify the smallest possible behavior of your code, hence the name “unit”. The idea is that the unit tests will provide detailed verification of your code, so if something breaks later on you can trace it back to the source.
 
We’ll start with ```RoomTest```. Go to the bottom of the file and you’ll see the skeleton mostly filled in. Follow the instructions there to finish the rest of it. Hint: for the Unicode method, your answer will look something like ```self.room.field_name + “_” + self.room.field_name```.
 
Now find ```DelegateTest``` and fill in ```test_unique```.
 
Now the fun part. At the very bottom is ```RoomCommentTest```. And it has very bare-bones skeleton code (get it? get it?). Your job is to fill this in without any extra guidance, but you should mostly be doing what you did above. Think through what each method is trying to accomplish based off what you saw in other tests.
 
Now go to a terminal and from your Huxley directory type:
 
```
python manage.py test huxley.core.test.test_models
```
 
Did anything break? If so, it sounds like you need to fix your code! Make sure the unit test is correct first, and, if it is, find the place in models.py the test corresponds to. Note: DO NOT change the unit test until you pass it. Only change the unit test if there is a problem with the test itself. No taking the easy way out here.

There are plenty more tests we could add if we wanted to; unit tests always involve design decisions on what to include and what not to. It comes down to one question: what's going to be the most confusing later on if it breaks? It does not come down to: "writing unit tests is so boring please make it stop if you have any pity on my soul!" (I guarantee you will say almost these exact words at least a few hundred times in your coding career). Unit tests may be boring to do, but they are the backbone of any major codebase and you will be glad you wrote them.
 
Step 8
 
Commit your code changes and push them to your local repository now, if you haven’t been doing that already. (You should do this as often as possible. Feel shame now. Deep shame. You forgot to commit, didn’t you? And what is life without commitment?).