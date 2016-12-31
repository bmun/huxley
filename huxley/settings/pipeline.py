# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).


PIPELINE = {
    'COMPILERS': (
        'huxley.utils.pipeline.PySCSSCompiler',
    ),

    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',

    'STYLESHEETS': {
        'huxley': {
            'source_filenames': (
                'scss/*.scss',
            ),
            'output_filename': 'css/huxley.css',
        },
    },
}
