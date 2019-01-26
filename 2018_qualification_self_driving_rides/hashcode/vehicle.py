# -*- coding: utf-8 -*-
import heapq

import hashcode


class Vehicle(object):
    """A Vehicle can drive rides.

    Each instance keep its own heap of rides, with the ride having the best score
    at the root. Use the method ´assign_best_next_ride()´ to assign the ride with
    the highest score to the vehicle.

    Args:
        rides: iterable of Ride instances. If you instantiate multiple Vehicles
               with the same staring intersection, it's recommended to pass it only
               once and then copy the `available_rides` heap to the other instances.
        row: the row of the start intersection of the Vehicle. Default: 0
        column: the column of the start intersection of the Vehicle. Default: 0
    """

    def __init__(self, rides=None, row=0, col=0):
        # Starting intersection of the vehicle
        self.start_intersection = hashcode.Intersection(row, col)
        # Intersection at which the vehicle is available once it drove
        # all its scheduled rides
        self.end_intersection = hashcode.Intersection(row, col)
        # Step at which the vehicle is available to drive a new ride
        self.driving_time = 0
        # Ordered list of rides scheduled for this vehicle
        self.scheduled_rides = []

        # heap of all the unassigned rides
        self.available_rides = self.evaluate_rides(rides) if rides else []

    def evaluate_rides(self, rides):
        """Build the heap of available rides.

        This method must be called each time a ride gets assigned to the vehicle.
        """
        tmp = []
        for ride in rides:
            score = self.ride_score(ride)
            if score is not None:
                heapq.heappush(tmp, (score, ride))
        return tmp

    def ride_score(self, ride):
        """Return the score of a ride based on the rides already scheduled.

        The algorithm to compute the score is quite simple and probably not optimal.
        It compares the amount of points rewarded with the time spent to drive (and wait)
        to the start of the ride.

        A small (negative) score is a better score.
            - score < 0:  reward is bigger than the investment
            - score == 0: reward is the same as the investment
            - score > 0:  reward is smaller than the investment

        An improvement idea is to take into account the latest_finish of a ride, to
        schedule the ones with an earlier latest_finish first.

        Returns:
            The score of the ride (low is better) or None if the ride cannot
            be finished on time.
        """
        transit_time = hashcode.distance(self.end_intersection, ride.start_intersection)

        # Don't bother driving it if it cannot be finished on time
        if ride.latest_finish - ride.distance <= self.driving_time + transit_time:
            return None

        waiting_time = ride.earliest_start - (self.driving_time + transit_time)
        bonus = ride.bonus if waiting_time >= 0 else 0
        # Negative waiting time isn't a thing, set it to zero
        waiting_time = waiting_time if waiting_time > 0 else 0

        investment = transit_time + waiting_time
        reward = ride.distance + bonus

        return investment - reward

    def assign_best_next_ride(self):
        """Assign the ride with the lowest score to this vehicle."""
        score, ride = self.best_next_ride(pop=True)

        if not ride:
            return

        ride.vehicle = self

        # Take this ride into account for the total driving time
        self.driving_time += hashcode.distance(self.end_intersection, ride.start_intersection)
        if self.driving_time < ride.earliest_start:
            self.driving_time = ride.earliest_start
        self.driving_time += ride.distance

        # "Move" the vehicle to the end intersection of this ride
        self.end_intersection = ride.end_intersection

        self.scheduled_rides.append(ride)
        self.available_rides = self.evaluate_rides([r[1] for r in self.available_rides])

    def best_next_ride(self, pop=False):
        """Return the score and best next ride for this vehicle.

        The ride with the best score could have been assigned to another vehicle,
        that's why best_next_ride() checks its status first and always return the
        ride with the best score, or (None, None) if no more rides are available.

        Args:
            pop: Should the ride be removed from heap? Default: False

        Returns:
            A tuple (score, Ride) or (None, None) if no ride more ride are available.
        """
        while True:
            if not self.available_rides:
                return None, None

            score, ride = self.available_rides[0]

            # Remove the rides already assigned to a vehicle from the heap
            if ride.vehicle:
                heapq.heappop(self.available_rides)
                continue

            if pop:
                heapq.heappop(self.available_rides)

            return score, ride

    def points(self):
        """Return the score awarded to the rides driven by this vehicle.

        Bonus points are awarded if the ride starts on time. Either if the vehicle
        gets there right on time or if it was there in advance.
        """
        total = 0

        position = self.start_intersection
        step = 0
        for ride in self.scheduled_rides:
            # Transit to the start of the ride
            step += hashcode.distance(position, ride.start_intersection)
            position = ride.start_intersection

            # Don't start the ride before ride.earliest_start
            waiting_time = ride.earliest_start - step
            if waiting_time > 0:
                step = ride.earliest_start
            bonus = ride.bonus if waiting_time >= 0 else 0

            # Drive the ride to the end
            step += ride.distance
            position = ride.end_intersection

            total += ride.distance + bonus

        return total
