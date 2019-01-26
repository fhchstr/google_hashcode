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

import hashcode
from hashcode import Scheduler


def main(data_set):
    n_vehicles, bonus, simulation_duration = hashcode.parse_summary(data_set)
    rides = hashcode.parse_rides(data_set, bonus, simulation_duration)
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


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except (IndexError, IOError) as e:
        print('usage: {} path_to_data_set_file'.format(sys.argv[0]))
        print('{}: {}'.format(e.__class__.__name__, e))
        sys.exit(1)
