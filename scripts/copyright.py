# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date
from os.path import abspath, dirname
from re import sub
from subprocess import check_output

HUXLEY_ROOT = abspath(dirname(dirname(__file__)))
COPYRIGHT_YEAR = '2011-%d' % date.today().year
COPYRIGHT_TEXT = '\n'.join(('# Copyright (c) %s Berkeley Model United Nations. All rights reserved.' % COPYRIGHT_YEAR,
                            '# Use of this source code is governed by a BSD License (see LICENSE).\n'))

def update_copyright():
    '''Add or update copyright headers for python files.'''
    files = check_output(['find', HUXLEY_ROOT, '-type', 'f']).split('\n')
    py_files = [f for f in files if f.endswith('.py')]

    for filename in py_files:
        with open(filename, 'r+') as f:
            contents = f.read()
            f.seek(0)
            if  not contents.startswith('# Copyright'):
                f.write(COPYRIGHT_TEXT)
                if len(contents) > 0:
                    f.write('\n')
                f.write(contents)
            else:
                f.write(sub('2011\-\d{4}', COPYRIGHT_YEAR, contents))

if __name__ == '__main__':
    update_copyright()
