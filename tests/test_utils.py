import unittest

from buxtor import utils


class PathComponentsTestCase(unittest.TestCase):
    def test_path_ending_with_normal_file(self):
        result = utils.path_components('/foo/bar/baz.py')

        self.assertEqual(result, ['/', 'foo', 'bar', 'baz.py'])

    def test_path_ending_with_directory_separator(self):
        result = utils.path_components('/foo/bar/')

        self.assertEqual(result, ['/', 'foo', 'bar'])

    def test_path_with_root(self):
        result = utils.path_components('/')

        self.assertEqual(result, ['/'])
