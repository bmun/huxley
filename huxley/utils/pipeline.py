# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from __future__ import absolute_import

from os.path import dirname

from django.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline_browserify.compiler import BrowserifyCompiler as BrowserifyCompilerBase


class PySCSSCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        root = dirname(settings.HUXLEY_ROOT)
        command = (
            '%s/scripts/pyscss.sh' % root,
            infile,
            outfile,
        )
        return self.execute_command(command, cwd=dirname(infile))


class BrowserifyCompiler(BrowserifyCompilerBase):
    '''Always recompile the entire JS codebase by setting `force` to True.
    This is because BrowserifyCompiler only takes the root file, and if
    it hasn't changed, it won't recompile anything.'''

    def compile_file(self, infile, outfile, outdated=False, force=False):
        return super(BrowserifyCompiler, self).compile_file(
            infile,
            outfile,
            outdated,
            True)
