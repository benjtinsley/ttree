import unittest
from rich_test_runner import RichTestRunner 

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    runner = RichTestRunner(verbosity=2)
    runner.run(suite)