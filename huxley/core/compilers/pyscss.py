# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings
from os.path import dirname
from pipeline.compilers import SubProcessCompiler

class PySCSSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        root = dirname(settings.HUXLEY_ROOT)
        command = '%s/scripts/pyscss.sh %s %s' % (root, infile, outfile)
        return self.execute_command(command, cwd=dirname(infile))

