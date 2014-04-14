#!/usr/bin/env python

# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huxley.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
