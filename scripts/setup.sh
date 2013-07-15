#!/usr/bin/env bash


function echo_green { echo "$(tput setaf 2)$1$(tput sgr0)"; }
function echo_yellow { echo "$(tput setaf 3)$1$(tput sgr0)"; }
function echo_red { echo "$(tput setaf 1)$1$(tput sgr0)"; }

function check_dependency {
    if ! hash $1 2>/dev/null; then
        echo_red >&2 "$2 not found. Get it by running \`sudo pip install $2\`. Aborting setup."
        exit 1
    else
        echo_green "$2 found."
    fi
}

echo "Beginning Huxley setup."
echo "Let's first check if you have both virtualenv and virtualenv wrapper..."

check_dependency virtualenv virtualenv
check_dependency virtualenvwrapper.sh virtualenvwrapper

echo "Looks good! Now we'll need to clone your repo. For that, I'll need your Github username."
echo -n "GitHub username: "
read username

git clone git@github.com:$(username)/huxley.git
cd huxley           
hub remote add upstream https://github.com/bmun/huxley.git

echo "Okay, next we'll install the Python dependencies from requirements.txt..."
mkvirtualenv huxley
workon huxley
pip install -r requirements.txt

# Initialize the database.
python manage.py syncdb # Make a superuser if prompted.
python manage.py migrate --fake
python manage.py loaddata countries committees advisor chair

# Collect static files.
python manage.py collectstatic --noinput

echo "And with that, you're ready to go!"
echo "Start the server with \`python manage.py runserver\`, and get hacking!"
echo "(Read the \"Submitting a Patch\" section in CONTRIBUTE when you're ready to submit your code."