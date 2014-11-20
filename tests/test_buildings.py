#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_buildings
----------------------------------

Tests for `buildings` module.
"""
import os

import unittest

from minepybs import buildings


class TestBuildings(unittest.TestCase):

    def setUp(self):
        pass

    def test_if_templates_dir_is_set_correctly(self):
        templates_dir = buildings.TemplateBuilding.TEMPLATES_DIR
        self.assertTrue(os.path.isdir(templates_dir), msg="TEMPLATES_DIR not set correctly.")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
