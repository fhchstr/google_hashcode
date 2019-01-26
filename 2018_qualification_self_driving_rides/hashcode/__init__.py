# -*- coding: utf-8 -*-
from collections import namedtuple

from ride import Ride
from scheduler import Scheduler
from vehicle import Vehicle

Intersection = namedtuple('Intersection', ['row', 'column'])


def distance(a, b):
    """Return the distance (= number of steps) between two intersections."""
    return abs(b.row - a.row) + abs(b.column - a.column)
