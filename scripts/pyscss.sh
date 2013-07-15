#!/usr/bin/env bash

# The latest version of pyscss outputs to stderr despite
# executing properly, and thus breaks the SCSS compiler.
# This is a light wrapper around pyscss that captures
# stderr output and checks the exit code, suppressing
# it if the program executed properly.

OUT=$(pyscss -o $2 $1 2>&1)
CODE=$?

if [ $CODE -ne 0 ]; then
    echo $OUT >&2
    exit $CODE
fi