# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

PIPELINE_COMPILERS = (
  'huxley.core.compilers.pyscss.PySCSSCompiler',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'

PIPELINE_CSS = {
    'huxley': {
        'source_filenames': (
            'css/*.css',
            'scss/core/*.scss',
            'scss/accounts/*.scss',
            'scss/advisors/*.scss',
            'scss/chairs/*.scss',
        ),
        'output_filename': 'css/huxley.css'
    },
}

PIPELINE_JS = {
    'huxley': {
        'source_filenames': (
            'js/core/*.js',
            'js/accounts/*.js',
            'js/advisors/*.js',
            'js/chairs/*.js',
        ),
        'output_filename': 'js/huxley.js'
    }
}
