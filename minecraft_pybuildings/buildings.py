# -*- coding: utf-8 -*-
import os

import yaml


class TemplateBuilding(object):
    """
        Main class that represents a template for any building
        using an yaml file.
    """
    TEMPLATES_DIR = 'templates'

    def __init__(self, template_name):
        super(TemplateBuilding, self).__init__()
        self.template_name = template_name

    def load(self):
        """
        Loads the given template building into a dict that represents it.
        """
        self.template = None
        template_path = os.path.join(self.TEMPLATES_DIR, self.template_name)
        with open(template_path, 'r') as template_file:
            self.template = yaml.load(template_file)

        return self.template


class House(TemplateBuilding):
    """A simple 5x5 house"""

    def __init__(self, template_name="house.yml"):
        super(House, self).__init__(template_name=template_name)
