#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_buildings
----------------------------------

Tests for `buildings` module.
"""
import os

import unittest

import mclevel

from minepybs import buildings
from box import BoundingBox


class TestBuildings(unittest.TestCase):

    def setUp(self):
        pass

    def test_if_templates_dir_is_set_correctly(self):
        "check if the templates_dir was set relative to the buildings.py file"
        templates_dir = buildings.TemplateBuilding.TEMPLATES_DIR
        self.assertTrue(os.path.isdir(templates_dir), msg="TEMPLATES_DIR not set correctly.")

    def test_get_block_with_only_id(self):
        "test if the 'get_block' can pass the correct info if only the id is present"

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
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '5', '1']
                        ]
                        }
        template_building = buildings.TemplateBuilding('template_test')
        template_building.template = template_test
        self.assertEquals(
            template_building.get_block(x=0, y=0, z=0),
            {'id': 1, 'pivot': None, 'n': None}
        )

        self.assertEquals(
            template_building.get_block(x=2, y=1, z=3),
            {'id': 5, 'pivot': None, 'n': None}
        )

    def test_get_block_with_dict(self):
        "test if the 'get_block' can pass the correct info if a dict is present"

        template_test = {0:
                        [
                            [{'id': '1'}, '2', '3', '4'],
                            [{'id': '1', 'n': 2}, '1', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1']
                        ],
                        1:
                        [
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', '1', '1'],
                            ['1', '1', {'id': '5', 'pivot': 'x'}, '1']
                        ]
                        }
        template_building = buildings.TemplateBuilding('template_test')
        template_building.template = template_test
        self.assertEquals(
            template_building.get_block(x=0, y=0, z=0),
            {'id': 1, 'pivot': None, 'n': None}
        )
        self.assertEquals(
            template_building.get_block(x=0, y=0, z=1),
            {'id': 1, 'pivot': None, 'n': 2}
        )

        self.assertEquals(
            template_building.get_block(x=2, y=1, z=3),
            {'id': 5, 'pivot': 'x', 'n': None}
        )

    def test_get_next_block(self):
        "test if get_next_block really works"

        template_test = {0:
                        [
                            ['1', '2'],
                            ['3', '4'],
                        ],
                        1:
                        [
                            ['5', '6'],
                            ['7', '8'],
                        ]
                        }
        template_building = buildings.TemplateBuilding('template_test')
        template_building.template = template_test
        for i in xrange(1, 9):
            self.assertEquals(
                template_building.get_next_block(),
                {'id': i, 'pivot': None, 'n': None}
            )
        self.assertIsNone(template_building.get_next_block())
        self.assertIsNone(template_building.get_next_block())

    def tearDown(self):
        pass


class TestHouse(unittest.TestCase):

    def setUp(self):
        self.test_level = mclevel.fromFile("tests/test_map/testworld/level.dat")

    def test_can_load_a_house_template(self):
        "test if can load the 'house.yml' file"
        house = buildings.House()
        self.assertIsNotNone(house.load())

    def test_generate_house_do_something(self):
        "test if a house is really doing something in the test map"
        build_pos = (731, 3, 1454)

        house = buildings.House()
        box_size = house.load()['size']

        bbox = BoundingBox(origin=build_pos, size=box_size)

        chunk_positions = list(bbox.chunkPositions)

        # get info about the blocks in the affected chunks
        old_chunks_blocks = []
        for chunk_pos in chunk_positions:
            chunk = self.test_level.getChunk(*chunk_pos)
            chunk_blocks_cp = chunk.Blocks.copy()
            old_chunks_blocks.append(chunk_blocks_cp)

        house.generate(self.test_level, *build_pos)

        # check all the new chunks blocks, against
        # the old ones (before the generation)
        old_chunk_iter = 0
        for chunk_pos in chunk_positions:
            chunk = self.test_level.getChunk(*chunk_pos)
            old_chunk_blocks = old_chunks_blocks[old_chunk_iter]
            verify = old_chunk_blocks == chunk.Blocks
            # assert that shouldn't have all blocks
            # the same before generating the building
            self.assertFalse(verify.all())
            old_chunk_iter += 1

    def tearDown(self):
        # ensure the file locks are closed
        self.test_level.close()


class TestTwoWaysRailSystem(unittest.TestCase):

    def setUp(self):
        # self.test_level = mclevel.fromFile("tests/test_map/testworld/level.dat")
        pass

    def test_calculate_direction_on_north_sount(self):
        point_a = [0, 0, 0]
        point_b = [2, 1, 3]
        rail_system = buildings.TwoWaysRailSystem('level', point_a, point_b)
        rail_system.calculate_direction()
        self.assertEquals(rail_system.direction, 1)

    def tearDown(self):
        # ensure the file locks are closed
        # self.test_level.close()
        pass

if __name__ == '__main__':
    unittest.main()
