# Contribute to Huxley

We're really excited for you to start contributing to Huxley. Below are the  steps to help you get started and submit a patch.

**NOTE**: These instructions assume you're developing on Mac OS X. If you're on another platform, please consult the setup guides (coming soon!).

## Getting Started
Begin by creating a fork of this repository. Go to the top-right of this repository page and click "Fork" (read Github's [guide](http://help.github.com/forking/) for a refresher on forking. If you're new to GitHub, remember to [set up SSH keys](https://help.github.com/articles/generating-ssh-keys) as well).

Then, if you're developing on Mac OS X, execute the following command:

	$ \curl -L -K https://raw.github.com/bmun/huxley/master/scripts/setup.sh | bash

And that's it! Everything wil be taken care of automatically. **This script assumes that you have virtualenv and virtualenv wrapper installed.** The [detailed setup steps](docs/setup/OSX.md) are given for reference, in case you'd like to customize your setup.

## Submitting a Patch
We use [Fabric](http://www.fabfile.org/) to automate many of the tasks during development. These help to create/destroy branches, open pull requests, update the AUTHORS file, and update copyright headers.

1. Create a new topic branch. Make the name short and descriptive: `fab feature:my-branch-name`.
2. Make your changes! Feel free to commit often.
3. Rebase your topic branch onto the latest upstream with `fab update`.
4. Open/update a pull request for your changes with `fab submit`. You can do this as many times as you like!
5. After your pull request has been merged or closed, clean up your branches with `fab finish`.

### Tips
- **Use one topic branch per feature!** This will allow you to better track where your various changes are, and will make it easier for us to merge features into the main repository.
- **Follow style guidelines!** Make sure you've read the code style guidelines before making your changes.
- **Test your code!** If you add new functions, be sure to write unit tests for them, and modify existing unit tests already.
- **Update the documentation!** If you feel that your change warrants a change to the current documentation, please do update the documentation as well.
