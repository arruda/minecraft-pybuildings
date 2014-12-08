# -*- coding: utf-8 -*-
import os

import numpy
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

        if type(block_info) == type(dict()):
            block_info['id'] = int(block_info['id'])
            block_dict.update(block_info)
        else:
            block_dict['id'] = int(block_info)

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

    def generate(self, level, x, y, z):
        """
        Generate this building in this position,
        starting using the given coordinates as the (0,0,0)
        for the new building.
        """

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
            block_id = 0
            block_data = 0

            # get the block level's info only if there is a
            # block to be set
            if block['id'] > 0:
                block_name = self.template['legend'][str(block['id'])]['name']
                block_id = level.materials.get(block_name).ID
                # get the default block data,
                # or the specified in template (if present)
                block_data = int(self.template['legend'][str(block['id'])].get(
                    'block_data',
                    level.materials.get(block_name).blockData
                ))

            # change the block only if it's needed
            # so if the block id is -1, it will ignore it
            if block['id'] >= 0:
                level.setBlockAt(next_x, next_y, next_z, block_id)
                level.setBlockDataAt(next_x, next_y, next_z, block_data)

            block = self.get_next_block()

        for chunk_pos in chunk_positions:
            chunk = level.getChunk(chunk_pos[0], chunk_pos[1])
            chunk.chunkChanged()

        return level


class House(TemplateBuilding):
    """A simple 4x4 house"""

    def __init__(self, template_name="house.yml"):
        super(House, self).__init__(template_name=template_name)


class TwoWaysRailStationBase(TemplateBuilding):
    """
    A Two Ways Rail Station Base.
    This is used by the North-South, South-North,
    East-West and West-East.
    """

    def __init__(self, template_name):
        super(TwoWaysRailStationBase, self).__init__(template_name=template_name)

    def generate(self, level, x=0, y=0, z=0):
        """
        Calculate the position to put the station,
        positioning the station door(lower part) in front
        of the given position x, y and z.
        """
        y -= 3
        return super(TwoWaysRailStationBase, self).generate(level, x, y, z)


class TwoWaysRailStationNS(TwoWaysRailStationBase):
    """
    A Two Ways Rail Station from North-South/South-North.

    To change from North-South to South-North position one should
    pass the `flip=True` parameter when instantiating the class.
    By default `flip` is `False`.
    """

    def __init__(self, template_name="2ways_rail_station_n_s.yml", flip=False):
        self.flip = flip
        super(TwoWaysRailStationNS, self).__init__(template_name=template_name)

    def load(self):
        """
        Loads the given template, but flip it if necessary.
        """
        super(TwoWaysRailStationNS, self).load()
        if self.flip:
            size = self.template.get('size')
            for y in xrange(0, int(size[1])):
                m = self.template.get(y)
                # convert the blocks array to
                # to a numpy int array
                m_np = numpy.array(m, int)
                # rotate the matrix in 180 degrees
                m_np = numpy.rot90(m_np, k=2)

                # exchange the old matrix for the new one
                self.template[y] = m_np.tolist()

            # change the button block_data, so that
            # it faces the right direction
            self.template['legend']['7']['block_data'] = "1"

        # # exchange the x/z in size:
        # self.template['size'] = [size[2], size[1], size[0]]
        return self.template

    def generate(self, level, x=0, y=0, z=0):
        """
        Calculate the position to put the station,
        positioning the station door(lower part) in front
        of the given position x, y and z.
        """
        x -= 3

        if self.flip:
            z -= 6

        return super(TwoWaysRailStationNS, self).generate(level, x, y, z)


class RailWay(TemplateBuilding):
    """
    A closed rail way with a powered rail.
    This is just a one block rail part.
    If you want to build a path, then put many of
    this along till you reach the desired point.
    (doesn't include curves)
    """

    def __init__(self, template_name="rail_way_n_s.yml"):
        super(RailWay, self).__init__(template_name=template_name)

    def generate(self, level, x=0, y=0, z=0):
        """
        Calculate the position to put the railway,
        positioning the rail in at the given position x, y and z.
        """
        x -= 1
        y -= 2

        return super(RailWay, self).generate(level, x, y, z)


class TwoWaysRailSystem(object):
    """
    Creates a Rail system, that connects point A and point B.
    It will create a Two Ways Rail Station in each point, and connects
    them with Rail Ways for A->B travels and the other way around.
    """

    DIRECTIONS = {
        "north_south": 1,
        "west_east": 2,
        "south_north": 3,
        "east_west": 4,
    }

    def __init__(self, level, point_a, point_b):
        super(TwoWaysRailSystem, self).__init__()
        self.level = level
        self.point_a = point_a
        self.point_b = point_b

        self.direction = 0
        self.point_diff = [0, 0, 0]
        self.calculate_direction()

    def calculate_direction(self):
        """
        set the correct direction,
        """

        self.point_diff = [
            self.point_a[0] - self.point_b[0],
            self.point_a[1] - self.point_b[1],
            self.point_a[2] - self.point_b[2]
        ]

        most_diff_coord = 0

        # work with positive values for the comparisons
        mod = lambda x: x if x > 0 else x*-1

        # dont compare Y for now, not sure it will be any different
        # if mod(self.point_diff[1]) > mod(self.point_diff[most_diff_coord]):
        #     most_diff_coord = 1
        if mod(self.point_diff[2]) > mod(self.point_diff[most_diff_coord]):
            most_diff_coord = 2

        # check for the minimun distance for this Rail System
        # if mod(self.point_diff[most_diff_coord]) < MINIMUM:

        # is either a North-South or East-West case
        if self.point_diff[most_diff_coord] < 0:
            # it's East-west
            if most_diff_coord == 0:
                self.direction = self.DIRECTIONS['east_west']
            # it's North-South
            else:
                self.direction = self.DIRECTIONS['north_south']

        # is either a South-North or West-East case
        elif self.point_diff[most_diff_coord] > 0:
            # it's West-East
            if most_diff_coord == 0:
                self.direction = self.DIRECTIONS['west_east']
            # it's South-North
            else:
                self.direction = self.DIRECTIONS['south_north']

    def generate_pa_rail_station(self):
        """
        generate the Rail Station for Point A
        """
        flip = False
        if self.direction == self.DIRECTIONS['south_north']:
            flip = True

        rail_station_a = TwoWaysRailStationNS(flip=flip)
        rail_station_a.load()
        rail_station_a.generate(self.level, *self.point_a)

    def generate_pb_rail_station(self):
        """
        generate the Rail Station for Point B
        """
        flip = True
        if self.direction == self.DIRECTIONS['south_north']:
            flip = False

        rail_station_b = TwoWaysRailStationNS(flip=flip)
        rail_station_b.load()
        rail_station_b.generate(self.level, *self.point_b)

    def generate(self):
        """
        Generate the Rail System
        """
        self.generate_pa_rail_station()
        self.generate_pb_rail_station()

        return self.level

    def save_level(self):
        "save the level after what was generated"
        self.level.generateLights()
        self.level.saveInPlace()
        return self.level
