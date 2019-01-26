# -*- coding: utf-8 -*-
from collections import namedtuple

from ride import Ride
from scheduler import Scheduler
from vehicle import Vehicle

Intersection = namedtuple('Intersection', ['row', 'column'])


def distance(a, b):
    """Return the distance (= number of steps) between two intersections."""
    return abs(b.row - a.row) + abs(b.column - a.column)


def parse_summary(data_set):
    """Parse the first line from the data set and return the values we need to solve
       the challenge.

    The first line of the input file contains the following integer integer numbers
    separated by single spaces:
        - (ignored) number of rows of the grid
        - (ignored) number of columns of the grid
        - number of vehicles in the fleet
        - (ignored) number of rides
        - per-ride bonus for starting the ride on time
        - number of steps in the simulation

    Args:
        data_set: path to the data set file

    Returns:
        A tuple (n_vehicles, ride_bonus, simulation_duration)
    """
    with open(data_set, 'r') as f:
        values = [int(v) for v in f.readline().split()]
        return values[2], values[4], values[5]

def parse_rides(data_set, bonus, simulation_duration):
    """Parse all lines, except the first, from the data set and return a list of Ride
       instances in the same order as they were read from the file.

    The subsequent lines of the input file describe the individual rides, from ride 0
    to ride N − 1.  Each line contains the following integer numbers separated by single
    spaces:
        - the row of the start intersection
        - the column of the start intersection
        - the row of the finish intersection
        - the column of the finish intersection
        - the earliest start
        - the latest finish

    Args:
        data_set: path to the data set file
        bonus: bonus value for a ride started on time
        simulation_duration: duration of the simulation (in steps)

    Returns:
        A list of Ride instances
    """
    keys = ('start_row', 'start_col', 'end_row', 'end_col', 'earliest_start', 'latest_finish')
    rides = []
    with open(data_set, 'r') as f:
        f.readline()  # Skip the first line

        for i, line in enumerate(f):
            values = [int(v) for v in line.split()]
            ride_properties = dict(zip(keys, values))
            ride_properties['identifier'] = i
            ride_properties['bonus'] = bonus
            ride_properties['simulation_duration'] = simulation_duration
            rides.append(Ride(**ride_properties))

    return rides
