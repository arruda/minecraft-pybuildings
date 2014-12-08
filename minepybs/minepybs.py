#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mclevel

from buildings import House, TwoWaysRailStationNS, RailWay


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


def create_rail_station_in_pos(level, x=0, y=0, z=0, flip=False):
    # level = mclevel.loadWorld("testworld")
    player_pos = (x, y, z)
    rail_station = TwoWaysRailStationNS(flip=flip)
    rail_station.load()
    level = rail_station.generate(level, x=player_pos[0], y=player_pos[1], z=player_pos[2])
    # level.generateLights()
    # level.saveInPlace()


def create_rail_way_in_pos(level, x=0, y=0, z=0):
    # level = mclevel.loadWorld("testworld")
    player_pos = (x, y, z)
    rail_way = RailWay()
    rail_way.load()
    level = rail_way.generate(level, x=player_pos[0], y=player_pos[1], z=player_pos[2])
    # level.generateLights()
    # level.saveInPlace()


if __name__ == "__main__":

    level = mclevel.loadWorld("testworld")
    dist = 50
    create_rail_station_in_pos(level, 733, 6, 1453)
    z_start = 1460
    z_end = z_start + dist
    for i in xrange(0, dist):
        create_rail_way_in_pos(level, 731, 5, z_start+i)
        create_rail_way_in_pos(level, 735, 5, z_start+i)

    create_rail_station_in_pos(level, 733, 6, z_end + 6, flip=True)
    level.generateLights()
    level.saveInPlace()
