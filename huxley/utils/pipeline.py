# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from __future__ import absolute_import

from os.path import dirname

from django.conf import settings
from pipeline.compilers import SubProcessCompiler


class PySCSSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        root = dirname(settings.HUXLEY_ROOT)
        command = '%s/scripts/pyscss.sh %s %s' % (root, infile, outfile)
        return self.execute_command(command, cwd=dirname(infile))

