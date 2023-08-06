import doctest
import unittest

from fake_memcached import fake_memcached


test_suite = unittest.TestSuite()
test_suite.addTest(doctest.DocTestSuite(fake_memcached))
unittest.TextTestRunner(verbosity = 2).run(test_suite)
