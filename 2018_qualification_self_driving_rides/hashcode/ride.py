# -*- coding: utf-8 -*-
import hashcode


class Ride(object):
    """A Ride is a drive between 2 intersections.

    The only modifiable attribute is 'vehicle', used to indicate if a Ride is assigned to a Vehicle.
    """

    def __init__(
        self,
        identifier,
        bonus,
        start_row,
        start_col,
        end_row,
        end_col,
        earliest_start,
        latest_finish,
        simulation_duration
    ):
        self.identifier = identifier
        self.bonus = bonus
        self.start_intersection = hashcode.Intersection(start_row, start_col)
        self.end_intersection = hashcode.Intersection(end_row, end_col)
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish if latest_finish < simulation_duration else simulation_duration

        self.distance = hashcode.distance(self.start_intersection, self.end_intersection)
        self.vehicle = None

    def __str__(self):
        return (
            '{0} {1.identifier} [{1.start_intersection.row}:{1.start_intersection.column} -> '
            '{1.end_intersection.row}:{1.end_intersection.column} (d={1.distance}) '
            'start={1.earliest_start}, finish={1.latest_finish}]'
        ).format(self.__class__.__name__, self)
