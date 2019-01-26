#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Author: Fabien Hochstrasser
# Date:   2019-01-23
#
# Solve the Google Hash Code qualification 2018 challenge.
#
# Usage: hashcode.py path_to_data_set_file
#
import sys

from hashcode import Ride, Scheduler


def main(data_set):
    n_vehicles, bonus, simulation_duration = parse_summary(data_set)
    rides = parse_rides(data_set, bonus, simulation_duration)
    scheduler = Scheduler(rides, n_vehicles)
    scheduler.dispatch()

    # Each line describing the rides of a vehicle must contain the following
    # integers separated by single spaces:
    #   - number of rides assigned to the vehicle
    #   - ride numbers assigned to the vehicle, in the order in which the
    #     vehicle will perform them
    for v in scheduler.vehicles:
        print('{} {}'.format(
            len(v.scheduled_rides),
            ' '.join([str(r.identifier) for r in v.scheduled_rides]),
        ))

    # Print the total score on STDERR to filter it easily from the output
    score = sum([v.points() for v in scheduler.vehicles])
    sys.stderr.write('score: {}\n'.format(score))


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


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except (IndexError, IOError) as e:
        print('usage: {} path_to_data_set_file'.format(sys.argv[0]))
        print('{}: {}'.format(e.__class__.__name__, e))
        sys.exit(1)
