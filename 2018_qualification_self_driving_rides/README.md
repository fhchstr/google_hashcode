# 2018 Qualification Round
Millions of people commute by car every day; for example, to school or to their workplace.
Self-driving vehicles are an exciting development for transportation. They aim to make traveling by car safer
and more available while also saving commuters time.
In this competition problem, we’ll be looking at how a fleet of self-driving vehicles can efficiently get
commuters to their destinations in a simulated city.

## My implementation
I decided to rate each ride and give them a score for each vehicle, based on its location (=intersection) and time (=step). A ride with a high score is a ride which:
* has a long distance
* is close to the current intersection
* starts in a reasonable time (or started already)

Bonus points are rewarded if the ride starts exactly on time, so it's worth waiting a few steps (but not too many) for the ride to start.

This is implemented using a heap because it's a very efficient data structure to get the ride with the best score.

Once a ride gets assigned to a vehicle, the score of all the other possible rides must be re-calculated based on the new location and step of the vehicle. This must only be done for the vehicle which got a new ride assigned to him. The position/step of the other vehicles didn't change, so the score of their rides didn't change either.

### Score calculation
A good score is a low (negative) score because a min-heap is used.
```
investment = transit_time + waiting_time
reward     = distance + bonus

score = investment - reward

  - score < 0:  reward is bigger than the investment
  - score == 0: reward is the same as the investment
  - score > 0:  reward is smaller than the investment


good
----
distance: distance of the ride
bonus: points awarded if the ride starts on time

bad
---
transit_time: number of steps required to move from the current position to the start of the ride
waiting_time: number of steps spent waiting for the ride to start
```

### Scheduling

To schedule the rides as efficiently as possible, the ride with the best score among all the vehicles is scheduled next.
This is also implemented using a heap. This one contains only the best score of each vehicle.
```
while rides still not assigned:
    take the ride with the best score among all the vehicles
    assign it to the corresponding vehicle
    re-calculate the score of all the rides for this vehicle
```

## Result
Here is how you can run the script for each data set.
```bash
$ mkdir -p output;
for f in data_sets/*; do \
    start=$SECONDS; \
    echo -n "${f}: "; \
    python hashcode.py $f > "output/$(basename $f .in).out"; \
    echo "in $(($SECONDS - $start)) seconds";
done
```
Here is the output (the files to submit are in the `output/` directory.
```
data_sets/a_example.in: score: 10
in 0 seconds
data_sets/b_should_be_easy.in: score: 175352
in 0 seconds
data_sets/c_no_hurry.in: score: 15385206
in 309 seconds
data_sets/d_metropolis.in: score: 10854665
in 174 seconds
data_sets/e_high_bonus.in: score: 20557945
in 264 seconds
```
Total: **46973178** points which corresponds to rank 530/3012 ([Scoreboard](https://codingcompetitions.withgoogle.com/hashcode/archive/2018)).

## Improvements
* The score formula is pretty naive and doesn't prioritize the rides which must be finished early
* Instead of "just" taking the ride with the best score, some smart brute-force could be done
  * Bulding a graph and using a shortest path algorithm is probably a good solution
