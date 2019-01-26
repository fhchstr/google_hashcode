# -*- coding: utf-8 -*-
import heapq

from vehicle import Vehicle


class Scheduler(object):
    """A Scheduler is responsible to dispatch Rides in its pool of Vehicles."""

    def __init__(self, rides, n_vehicles):
        # All the vehicles start at the same time at the same position, this means
        # they would all compute the same score for all the rides. To prevent
        # computing the same thing multiple times, the rides are evaluated only
        # once and the resulting heap is *copied* on the other vehicles.
        vehicle = Vehicle(rides)
        self.vehicles = [vehicle]
        for _ in xrange(1, n_vehicles):
            v = Vehicle()
            v.available_rides = vehicle.available_rides[:]
            self.vehicles.append(v)

    def dispatch(self):
        """Dispatch the rides among the vehicles.

        Each vehicle has its own heap where the possible next rides are referenced,
        the one with the best score being at the root. To decide which ride should be
        assigned to which vehicle next, the dispatch() method takes the ride with the
        best score among all the vehicles.

        To quickly find which ride has the best score, the dispatch() method uses its
        own heap which contains only the best score of each vehicle.
        """
        rides = []
        for vehicle in self.vehicles:
            score, _ = vehicle.best_next_ride()
            heapq.heappush(rides, (score, vehicle))

        while rides:
            _, vehicle = heapq.heappop(rides)
            vehicle.assign_best_next_ride()
            score, ride = vehicle.best_next_ride()
            if ride:
                heapq.heappush(rides, (score, vehicle))
