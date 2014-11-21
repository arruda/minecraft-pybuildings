# -*- coding: utf-8 -*-
import os

import yaml

from box import BoundingBox


class TemplateBuilding(object):
    """
        Main class that represents a template for any building
        using an yaml file.
    """
    TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

    def __init__(self, template_name):
        super(TemplateBuilding, self).__init__()
        self.template_name = template_name
        self.template = None
        self._current_block_pos = None
        self.size = None

    def load(self):
        """
        Loads the given template building into a dict that represents it.
        """
        self.template = None
        template_path = os.path.join(self.TEMPLATES_DIR, self.template_name)
        with open(template_path, 'r') as template_file:
            self.template = yaml.load(template_file)

        return self.template

    def get_block(self, x=0, y=0, z=0):
        """
        Read the information from the block X, Y, Z
        Where:

            * X: the colums in the yaml file.
            * Z: are the lines in the yaml file.
            * Y: each entry in the yaml file.

        If the information in this 'position' is a string, then
        will return the int that represents this string (the ID of the block)

        if is a dictionary, then will try to retrieve the datas:

            * id: the block's id;
            * n: the number of times this block is repeated in this line;
            * pivot: integer that indicates if this position should be marked.

        this can be used to mark places where you want to
        place other sub-structures inside this structure when rendering.
        """
        block_info = self.template[y][z][x]
        block_dict = {
            'id': None,
            'n': None,
            'pivot': None
        }

        if type(block_info) == type(str()):
            block_dict['id'] = int(block_info)
        else:
            block_dict = block_info

        return block_dict

    def get_next_block(self):
        "get the next block to build in a map"
        next_pos = []
        if self._current_block_pos:
            next_pos.extend(self._current_block_pos)

            # x + 1
            next_pos[2] += 1
            if not next_pos[2] < len(self.template[next_pos[0]][next_pos[1]]):
                # z + 1
                next_pos[2] = 0
                next_pos[1] += 1
                if not next_pos[1] < len(self.template[next_pos[0]]):
                    # y + 1
                    next_pos[1] = 0
                    next_pos[0] += 1
                    if not self.template.get(next_pos[0]):
                        # reach the end there is no more blocks
                        return None
        else:
            self._current_block_pos = [0, 0, 0]
            next_pos.extend(self._current_block_pos)

        self._current_block_pos = next_pos
        return self.get_block(x=next_pos[2], z=next_pos[1], y=next_pos[0])

    def generate(self, level, x=0, y=0, z=0):
        """
        Generate this building in this chunk,
        starting using the given coordinates (relative to the chunk) as the (0,0,0)
        for the new building.
        """

        if not level or not x or not y:
            raise Exception(msg="Should pass the level, and (x,y,z) coordinates")

        size = self.template['size']
        bbox = BoundingBox(origin=(x, y, z), size=size)
        # bbox = bbox.chunkBox(level)
        chunk_positions = bbox.chunkPositions
        # ensure no chunks that might be needed won't be left undone
        created_chunks = level.createChunksInBox(bbox)
        block = self.get_next_block()
        while block:
            next_x = int(x + self._current_block_pos[2])
            next_z = int(z + self._current_block_pos[1])
            next_y = int(y + self._current_block_pos[0])
            block_name = self.template['legend'][str(block['id'])]

            block_id = level.materials.get(block_name).ID
            level.setBlockAt(next_x, next_y, next_z, block_id)
            block = self.get_next_block()

        for chunk_pos in chunk_positions:
            chunk = level.getChunk(chunk_pos[0], chunk_pos[1])
            chunk.chunkChanged()

        return level


class House(TemplateBuilding):
    """A simple 4x4 house"""

    def __init__(self, template_name="house.yml"):
        super(House, self).__init__(template_name=template_name)
