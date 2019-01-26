import os
import unittest

import hashcode
from hashcode import distance, Intersection

TEST_INPUT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.in')

def point(coordinates):
    """Return an Intersection instance with the given coordinates."""
    return Intersection(*[int(c) for c in coordinates.split(':')])


class TestHashcode(unittest.TestCase):
    """Test the entry script and the functions defined in the package."""

    def test_distance_same_intersection(self):
        self.assertEqual(distance(point('0:0'), point('0:0')), 0)
        self.assertEqual(distance(point('2:1'), point('2:1')), 0)

    def test_distance_same_row(self):
        self.assertEqual(distance(point('0:0'), point('0:3')), 3)
        self.assertEqual(distance(point('0:3'), point('0:0')), 3)

    def test_distance_same_column(self):
        self.assertEqual(distance(point('2:7'), point('8:7')), 6)
        self.assertEqual(distance(point('8:7'), point('2:7')), 6)

    def test_distance_upper_right(self):
        self.assertEqual(distance(point('3:2'), point('5:6')), 6)
        self.assertEqual(distance(point('1:5'), point('3:7')), 4)

    def test_distance_upper_left(self):
        self.assertEqual(distance(point('3:6'), point('4:3')), 4)
        self.assertEqual(distance(point('5:8'), point('7:2')), 8)

    def test_distance_lower_left(self):
        self.assertEqual(distance(point('2:6'), point('0:3')), 5)
        self.assertEqual(distance(point('5:2'), point('3:1')), 3)

    def test_distance_lower_right(self):
        self.assertEqual(distance(point('4:3'), point('2:5')), 4)
        self.assertEqual(distance(point('7:0'), point('6:5')), 6)

    def test_parse_summary(self):
        n_vehicles, bonus, simulation_duration = hashcode.parse_summary(TEST_INPUT)
        self.assertEqual(n_vehicles, 3)
        self.assertEqual(bonus, 1)
        self.assertEqual(simulation_duration, 25)

    def test_parse_rides(self):
        bonus = 3
        duration = 10
        rides = hashcode.parse_rides(TEST_INPUT, bonus, duration)

        self.assertEqual(len(rides), 3)
        # Each ride has its own identifier
        self.assertEqual(rides[0].identifier, 0)
        self.assertEqual(rides[1].identifier, 1)
        self.assertEqual(rides[2].identifier, 2)

        # Test the start and end intersections
        self.assertEqual(rides[0].start_intersection, point('0:0'))
        self.assertEqual(rides[0].end_intersection, point('3:4'))
        self.assertEqual(rides[1].start_intersection, point('1:1'))
        self.assertEqual(rides[1].end_intersection, point('2:3'))
        self.assertEqual(rides[2].start_intersection, point('4:4'))
        self.assertEqual(rides[2].end_intersection, point('4:5'))

        # Test the distance
        self.assertEqual(rides[0].distance, 7)
        self.assertEqual(rides[1].distance, 3)
        self.assertEqual(rides[2].distance, 1)

        # All the rides should have the same bonus value
        self.assertEqual({r.bonus for r in rides}, set([bonus]))

        # latest_finish cannot be higher than simulation_duration
        self.assertTrue(max([r.latest_finish for r in rides]) <= duration)
