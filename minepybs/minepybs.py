#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mclevel

from buildings import House


def create_house_in_player_pos():
    level = mclevel.loadWorld("New World")
    player_pos = level.getPlayerPosition()
    house = House()
    house.load()
    level = house.generate(level, x=player_pos[0], y=player_pos[1], z=player_pos[2])
    level.saveInPlace()


def create_house_in_pos(x=0, y=0, z=0):
    level = mclevel.loadWorld("New World")
    player_pos = (x, y, z)
    house = House()
    house.load()
    level = house.generate(level, x=player_pos[0], y=player_pos[1], z=player_pos[2])
    level.saveInPlace()


if __name__ == "__main__":

    create_house_in_pos(-259, 63, 195)
