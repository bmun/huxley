from datetime import date
from os.path import abspath, dirname
from re import sub
from subprocess import check_output

HUXLEY_ROOT = abspath(dirname(dirname(__file__)))
COPYRIGHT = '2011-%d' % date.today().year

files = check_output(['find', HUXLEY_ROOT, '-type', 'f']).split('\n')
py_files = [f for f in files if f.endswith('.py')]

for filename in py_files:
    with open(filename, 'r+') as f:
        contents = f.read()
        f.seek(0)
        f.write(sub('2011\-\d{4}', COPYRIGHT, contents))
