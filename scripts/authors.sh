#!/usr/bin/env sh

# Generate an alphabetized AUTHORS file based on git log.

git log --format='%aN <%aE>' | sort -u > AUTHORS
