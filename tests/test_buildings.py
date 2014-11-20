#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_minepybs
----------------------------------

Tests for `minepybs` module.
"""
import os

import unittest

from minepybs import buildings


class TestMinepybs(unittest.TestCase):

    def setUp(self):
        pass

    def test_can_load_from_correct_path(self):
        templates_dir = buildings.TemplateBuilding.TEMPLATES_DIR
        self.assertTrue(os.path.isdir(templates_dir), msg="TEMPLATES_DIR not set correctly.")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
