# -*- coding: utf-8 -*-
import os

import yaml


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

            * X: are the lines in the yaml file.
            * Y: the colums in the yaml file.
            * Z: each entry in the yaml file.

        If the information in this 'position' is a string, then
        will return the int that represents this string (the ID of the block)

        if is a dictionary, then will try to retrieve the datas:

            * id: the block's id;
            * n: the number of times this block is repeated in this line;
            * pivot: integer that indicates if this position should be marked.

        this can be used to mark places where you want to
        place other sub-structures inside this structure when rendering.
        """
        block_info = self.template[z][x][y]
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


class House(TemplateBuilding):
    """A simple 4x4 house"""

    def __init__(self, template_name="house.yml"):
        super(House, self).__init__(template_name=template_name)
