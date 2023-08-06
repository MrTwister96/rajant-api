# run_tests.py
import unittest

if __name__ == "__main__":
    # This will discover all tests in the 'tests' directory and run them.
    test_suite = unittest.defaultTestLoader.discover('tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
