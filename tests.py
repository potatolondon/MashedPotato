#!/usr/bin/env python

import unittest
from mashed_potato import get_paths_from_configuration, path_matches_regexps

class ConfigurationTest(unittest.TestCase):
    def test_comments_ignored(self):
        path_regexps = get_paths_from_configuration("/", "# foo \n# bar")
        self.assertEqual(path_regexps, [])

    def test_blank_lines_ignored(self):
        path_regexps = get_paths_from_configuration("/", "# \n # ")
        self.assertEqual(path_regexps, [])

    def test_regexp_number(self):
        path_regexps = get_paths_from_configuration("/", "foo\nbar\nbaz")
        self.assertEqual(len(path_regexps), 3)


class RegexpMatchingTest(unittest.TestCase):
    def test_simple_regexp(self):
        path_regexps = get_paths_from_configuration("/", "foo")
        self.assertTrue(path_matches_regexps("/foo", path_regexps))

    def test_complex_regexp(self):
        path_regexps = get_paths_from_configuration("/", "abc/[^/]+/ghi")
        self.assertTrue(path_matches_regexps("/abc/def/ghi", path_regexps))


if __name__ == '__main__':
    unittest.main()
