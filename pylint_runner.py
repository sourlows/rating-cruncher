import argparse
from pylint.lint import Run
import sys

sys.path.insert(0, 'C:\\Program Files (x86)\\Google\\google_appengine')
sys.path.insert(0, 'src/')
sys.path.insert(0, 'src/lib/')

sys.path.insert(0, 'test/')
sys.path.insert(0, 'test/lib/')

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', action='store_true', help='Run pylint on the source code.')
PARSER.add_argument('-t', action='store_true', help='Run pylint on the test code.')

ARGS = PARSER.parse_args()
if ARGS.s:
    PYLINTRC = 'src/pylintrc'
    Run(['--rcfile=src\\pylintrc', 'src\\app'])
if ARGS.t:
    Run(['--rcfile=test\\pylintrc', 'test\\'])
