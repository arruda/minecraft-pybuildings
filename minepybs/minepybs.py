#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mclevel

from buildings import House, TwoWaysRailStationSN


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
    level.generateLights()
    level.saveInPlace()


def create_rail_station_in_pos(x=0, y=0, z=0, flip=False):
    level = mclevel.loadWorld("testworld")
    player_pos = (x, y, z)
    rail_station = TwoWaysRailStationSN(flip=flip)
    rail_station.load()
    level = rail_station.generate(level, x=player_pos[0], y=player_pos[1], z=player_pos[2])
    level.generateLights()
    level.saveInPlace()


if __name__ == "__main__":

    create_rail_station_in_pos(733, 6, 1453)
    # import pdb; pdb.set_trace()
    create_rail_station_in_pos(733, 6, 1466, flip=True)
