#!/usr/bin/env bash


function echo_green { echo "$(tput setaf 2)$1$(tput sgr0)"; }
function echo_yellow { echo "$(tput setaf 3)$1$(tput sgr0)"; }
function echo_red { echo "$(tput setaf 1)$1$(tput sgr0)"; }

function binary_exists {
	if hash $1 2>/dev/null; then
		return 0
	else
		return 1
	fi
}

function check_dependency {
    if ! binary_exists $1; then
        echo_red >&2 "$2 not found. Get it by running \`sudo pip install $2\`. Aborting setup."
        exit 1
    else
        echo_green "$2 found."
    fi
}

echo_green "Beginning Huxley setup."
echo "Let's first check if you have both virtualenv and virtualenv wrapper..."

check_dependency virtualenv virtualenv
check_dependency virtualenvwrapper.sh virtualenvwrapper

echo "Looks good! Now we'll need to clone your repo. For that, I'll need your Github username."
echo -n "GitHub username: "
read username

git clone git@github.com:$(username)/huxley.git
cd huxley
git remote add upstream https://github.com/bmun/huxley.git

echo "Okay, next we'll install the Python dependencies from requirements.txt..."
mkvirtualenv huxley
workon huxley
pip install -r requirements.txt

echo "Then, we'll initialize your database and process static files..."
python manage.py syncdb # Make a superuser if prompted.
python manage.py migrate
python manage.py loaddata countries committees advisor chair
python manage.py collectstatic --noinput

if ! binary_exists hub; then
	echo_yellow "Looks like you don't have hub installed. It's not required for Huxley, but it makes it easier for you to issue pull requests to GitHub."
	if binary_exists brew; then
		echo_yellow "Would you like to install hub now? (y/n)"
		read input
		if [[ $input == "y" ]]; then
			brew install hub
		else
			echo "Okay. You can install hub with \`brew install hub\`."
		fi
	else
		echo_yellow "If you want to install hub, you'll need Homebrew. Learn more at http://brew.sh."
	fi
fi

echo_green "And with that, you're ready to go!"
echo_green "Start the server with \`python manage.py runserver\`, and get hacking!"
echo_green "(Read the \"Submitting a Patch\" section in CONTRIBUTE when you're ready to submit your code."
