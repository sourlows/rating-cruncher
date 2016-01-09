import unittest
import sys

sys.path.insert(0, 'C:\\Program Files (x86)\\Google\\google_appengine')
sys.path.insert(0, 'Q:\\Applications\\GAE')
sys.path.insert(0, 'src/')
sys.path.insert(0, 'src/lib/')

test_loader = unittest.TestLoader()
tests = test_loader.discover('test/', '*_test.py')
unittest.runner.TextTestRunner(verbosity=1).run(tests)
