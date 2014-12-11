===============================
Minecraft-PyBuildings
===============================

.. image:: https://badge.fury.io/py/minepybs.png
    :target: http://badge.fury.io/py/minepybs

.. image:: https://travis-ci.org/arruda/minecraft-pybuildings.png?branch=master
    :target: https://travis-ci.org/arruda/minecraft-pybuildings

.. image:: https://coveralls.io/repos/arruda/minecraft-pybuildings/badge.png
    :target: https://coveralls.io/r/arruda/minecraft-pybuildings


.. image:: https://pypip.in/d/minepybs/badge.png
    :target: https://pypi.python.org/pypi/minepybs

.. image:: https://readthedocs.org/projects/minecraft-pybuildings/badge/?version=latest
    :target: https://readthedocs.org/projects/minecraft-pybuildings/?badge=latest
    :alt: Documentation Status


Some predefined structures using yaml and pymclevel to build them on any minecraft map.

Usage
-----
Ex: Build a two-ways Rail System from point A to point B with a just a couple lines of code:

    import mclevel
    from minepybs.buildings import TwoWaysRailSystem


    level = mclevel.loadWorld("myworld")
    # X, Y and Z
    point_a = [100, 7, 1050]
    point_b = [100, 7, 1500]

    rail_system = TwoWaysRailSystem(level, point_a=point_a, point_b=point_b)
    rail_system.generate()
    rail_system.save_level()

This will give a rail station in point A, and point B, and two rail ways connecting them, one for A->B, and the other for B->A.
Also both rail ways are secure (closed and iluminated), powered and with view for the outside.

This is just an example, if you want to change something, you can just inherit the TwoWaysRailSystem and modify it for you case.


Install
-------

    pip install -e git+https://github.com/arruda/minecraft-pybuildings.git@master#egg=minepybs
    pip install -e git+https://github.com/mcedit/pymclevel.git@master#egg=pymclevel



* Free software: BSD license
* Documentation: https://minecraft-pybuildings.readthedocs.org.
