import sys
import unittest

from hashcode import Vehicle, Ride


def ride_factory(
    identifier=0, bonus=0, start_row=0, start_col=0, end_row=0, end_col=0,
    earliest_start=0, latest_finish=sys.maxint, simulation_duration=sys.maxint
):
    return Ride(
        identifier, bonus, start_row, start_col, end_row, end_col,
        earliest_start, latest_finish, simulation_duration
    )

class TestVehicle(unittest.TestCase):

    def test_ride_score(self):
        v = Vehicle()
        # Good scores
        self.assertEqual(v.ride_score(ride_factory(end_row=2, end_col=3)), -5)
        self.assertEqual(v.ride_score(ride_factory(bonus=3, end_row=1, end_col=1)), -5)
        self.assertEqual(v.ride_score(ride_factory(start_row=5, end_col=20)), -20)
        self.assertEqual(v.ride_score(ride_factory(bonus=15, start_row=5, end_col=20)), -20)
        self.assertEqual(v.ride_score(ride_factory(end_row=10, end_col=20, earliest_start=10)), -20)

        # Neutral scores
        self.assertEqual(v.ride_score(ride_factory(start_col=2, end_col=0)), 0)
        self.assertEqual(v.ride_score(ride_factory(end_row=5, end_col=5, earliest_start=10)), 0)

        # Bad scores
        self.assertEqual(v.ride_score(ride_factory(end_row=2, end_col=2, earliest_start=10)), 6)

        # Impossible rides
        self.assertIsNone(v.ride_score(ride_factory(start_row=4, earliest_start=2, latest_finish = 6)), None)

    def test_assign_best_next_ride(self):
        ride1 = ride_factory(start_row=0, start_col=0, end_row=10, end_col=12)
        ride2 = ride_factory(start_row=5, start_col=7, end_row=8, end_col=8)
        v = Vehicle([ride1, ride2])

        v.assign_best_next_ride()
        self.assertEqual(ride1.vehicle, v)
        self.assertEqual(v.scheduled_rides[0], ride1)
        self.assertEqual(v.driving_time, 22)
        self.assertEqual(v.end_intersection, ride1.end_intersection)
        self.assertEqual(len(v.available_rides), 1)

        v.assign_best_next_ride()
        self.assertEqual(ride2.vehicle, v)
        self.assertEqual(v.scheduled_rides[1], ride2)
        self.assertEqual(v.driving_time, 22 + (5 + 5) + (3 + 1))
        self.assertEqual(v.end_intersection, ride2.end_intersection)
        self.assertEqual(len(v.available_rides), 0)

        # Calling it again won't change a thing
        v.assign_best_next_ride()
        self.assertEqual(len(v.scheduled_rides), 2)


    def test_best_next_ride_without_available_rides(self):
        v = Vehicle()
        self.assertEqual(v.best_next_ride(), (None, None))

    def test_best_next_ride_with_one_ride(self):
        v = Vehicle([ride_factory(end_col=12)])
        score, ride = v.best_next_ride()  # Just read it, don't remove it
        self.assertEqual(score, -12)
        v.best_next_ride(pop=True)  # Read it and remove it
        self.assertEqual(v.best_next_ride(), (None, None))

    def test_best_next_ride_already_assigned(self):
        ride = ride_factory(end_col=12)
        v = Vehicle([ride])
        ride.vehicle = v
        self.assertEqual(v.best_next_ride(), (None, None))

    def test_points(self):
        ride1 = ride_factory(start_row=0, start_col=0, end_row=10, end_col=12, bonus=3)
        ride2 = ride_factory(start_row=5, start_col=7, end_row=8, end_col=8, earliest_start = 0, bonus=1)
        ride3 = ride_factory(start_row=0, start_col=0, end_row=15, earliest_start=50)

        v = Vehicle([ride2, ride1, ride3])
        self.assertEqual(v.points(), 0)

        # Drive ride1
        # distance = 22, bonus = 3
        v.assign_best_next_ride()
        self.assertEqual(v.points(), 22 + 3)  # = 25

        # Drive ride2
        # distance = 4, bonus = 0
        v.assign_best_next_ride()
        self.assertEqual(v.points(), 25 + 4 + 0)  # = 29

        # Drive ride3
        # distance = 15, bonus = 0
        v.assign_best_next_ride()
        self.assertEqual(v.points(), 29 + 15 + 0)  # = 44
