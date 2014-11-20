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
        "check if the templates_dir was set relative to the buildings.py file"
        templates_dir = buildings.TemplateBuilding.TEMPLATES_DIR
        self.assertTrue(os.path.isdir(templates_dir), msg="TEMPLATES_DIR not set correctly.")

    def test_can_load_a_house_template(self):
        "test if can load the 'house.yml' file"
        house = buildings.House()
        self.assertIsNotNone(house.load())

    def test_get_block_with_only_id(self):
        "test if the 'get_block' can pass the correct info info only the id is present"

        template_test = {0:
                        [
                            ['1', '2', '3', '4'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1']
                        ],
                        1:
                        [
                            ['1', '1', '1', '1'],
                            ['1', '5', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1']
                        ]
                        }
        template_building = buildings.TemplateBuilding('template_test')
        template_building.template = template_test
        self.assertEquals(
            template_building.get_block(x=0, y=0, z=0),
            {'id': 1, 'pivot': None, 'n': None}
        )

        self.assertEquals(
            template_building.get_block(x=1, y=1, z=1),
            {'id': 5, 'pivot': None, 'n': None}
        )

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
