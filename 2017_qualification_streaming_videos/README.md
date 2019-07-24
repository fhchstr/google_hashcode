# 2017 Qualification Round
Have you ever wondered what happens behind the scenes when you watch a YouTube video? As more and more people watch online videos (and as the size of these videos increases), it is critical that video-serving infrastructure is optimized to handle requests reliably and quickly.
This typically involves putting in place cache servers, which store copies of popular videos. When a user request for a particular video arrives, it can be handled by a cache server close to the user, rather than by a
remote data center thousands of kilometers away.

But how should you decide which videos to put in which cache servers?

### Task
Given a description of cache servers, network endpoints and videos, along with predicted requests for individual videos, decide which videos to put in which cache server in order to minimize the average waiting time for all requests.

More details on the [problem description](hashcode2017_qualification_task.pdf).

## My implementation
I noticed this problem is similar to the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem).
We have cache servers with limited capacity and videos which have:
* a size in MB
* a value (how much time / request is saved if it is hosted on a given cache server)

I decided to go for this implementation, knowing it would give me a close to optimal solution. After the fact, I'm thinking an approximaton algorithm would have given an acceptable score in a much shorter time. Maybe using a combinaison of both is even better (e.g. use the knapsack algorithm on a subset of the videos having the best reward/cost ratio).
Anyway, it was interesting to implement this algorithm and reduce its space complexity from `number of videos * cache cacpacity` to `2 * cache capacity`.

An important information to take into account is that if an endpoint is connected to 2 cache servers, hosting the video on the one with the higher latency will not help if it is already hosted on the one with the smaller latency.
That's why I decided to rate the cache servers by their potential latency gain and then apply the knapsack algorithm on each of them, starting from the one with the best potential latency gain.

### Knapsack algorithm
The idea of the algorithm is to build a bottom-up table which keeps track of the highest value for the items which can be included without going above the maximum capacity. Because it's bottom-up, the algorithm looks first at how much value can fit when the capacity is small (=1) and then continues until it evaluated the value which can fit in the actual capacity.

The only difference with the original knapsack algorithm, is that instead of just keeping track of the highest value (=time saved), the algorithm also keeps track of which videos were included in the set to get this result.

Here is how the knapsack algorithm works:

1. create a table of `1 + #videos` rows and `1 + capacity` columns filled with zeroes. Rows represent videos, columns represent remaining capacity. Some of the columns are not realistic depending on the input data set. With the example above, remaining capacity can never be 3 because there is no video of size=1 in the data set. But it's easier to compute those non-realistic cases than checking if they're realistic or not...
1. traverse the table column-by-column from the top left corner, skipping the row and column 0 (effectively starting at index `1, 1`).
1. For each cell:\
NOTE: the row indexes are shifted by `1` because the table has `1 + #videos` rows. So the video of line `i` is actually `videos[i-1]`
    1. Don't include the video if it doesn't fit in the remaining capacity. If the video isn't included, the value and remaining capacity remain the same. So just copy the value from the row above which corresponds to the value after including (or not) the previous video.
    1. If the video fits in the remaining capacity, it can either be included in the set, or not. So evaluate both scenarios and store the best result.

Given the example below, here is how the resulting table looks like. The best
value is the one in the bottom right cell. For simplicity, the tracking of
the videos isn't represented on the table.

Let's say we have 3 videos and a cache capacity of 4:
* v0(size=2, time_saved=2)
* v1(size=2, time_saved=2)
* v2(size=3, time_saved=3)


```
    table m    | 0 | 1 | 2 | 3 | 4
             --+---+---+---+---+---
             0 | 0 | 0 | 0 | 0 | 0
             --+---+---+---+---+---
       (v0)  1 | 0 | 0 | 2 | 2 | 2
             --+---+---+---+---+---
       (v1)  2 | 0 | 0 | 2 | 2 | 4
             --+---+---+---+---+---
       (v2)  3 | 0 | 0 | 2 | 3 | 4
```
Here is the step-by-step explanation of the algorithm used to fill the table. The coordinates are written as `m(row, column), the best choice is marked with an asterisk at the end of the line.

FIXME explain what happens if the score is the same.

**Column #1**\
`m(1, 1)`: v0 doesn't fit in capacity 1 -> `m(0, 1)` = 0 **(skip)**

`m(2, 1)`: v1 doesn't fit in capacity 1 -> `m(1, 1)` = 0 **(skip)**

`m(3, 1)`: v2 doesn't fit in capacity 1 -> `m(2, 1)` = 0 **(skip)**

**Column #2**\
`m(1, 2)`: v0 fits it capacity 2. Find the max between:
* `m(0, 2)` = 0 (skip)
* `v0.value + m(0, 2-v0.size)` = `v0.value + m(0, 0)` = 2 + 0 = 2 **(add)**

`m(2, 2)`: v1 fits in capacity 2. Find the max between:
* `m(1, 2)` = 2 **(skip)** FIXME
* `v1.value + m(1, 2-v0.size)` = `v1.value + m(1, 0)` = 2 + 0 = 2 **(add)** FIXME

`m(3, 2)`: v2 doesn't fit in capacity 2 -> `m(2, 2)` = 2 **(skip)**

**Column #3**\
`m(1, 3)`: v0 fits in capacity 3. Find the max between:
* `m(0, 3)` = 0 (skip)
* `v0.value + m(0, 3-v0.size)` = `v0.value + m(0, 1)` = 2 + 0 = 2 **(add)**

`m(2, 3)`: v1 fits in capacity 3. Find the max between:
* `m(1, 3)` = 2 **(skip)** FIXME
* `v1.value + m(1, 3-v1.size)` = `v1.value + m(1, 1)` = 2 + 0 = 2 **(add)** FIXME

`m(3, 3)`: v2 fits in capacity 3. Find the max between:
* `m(2, 3)` = 2 (skip)
* `v2.value + m(2, 3-v2.size)` = `v2.value + m(2, 0)` = 3 + 0 = 3 **(add)**

**Column #4**\
`m(1, 4)`: v0 fits in capacity 4. Find the max between:
* `m(0, 4)` = 0 (skip)
* `v0.value + m(0, 4-v0.size)` = `v0.value + m(0, 2)` = 2 + 0 = 2 **(add)**

`m(2, 4)`: v1 fits in capacity 4. Find the max between:
* `m(1, 4)` = 2 (skip)
* `v1.value + m(1, 4-v1.size)` = `v1.value + m(1, 2)` = 2 + 2 = 4 **(add)**

`m(3, 4)`: v2 fits in capcity 4. Find the max between:
* `m(2, 4)` = 4 **(skip)**
* `v2.value + m(2, 4-v2.size)` = `v2.value + m(2, 1)` = 3 + 0 (add)

As you might have noticed, only the previous row `index - 1` is used to compute the values of the next row. This means we don't need to allocate `#videos` rows. 2 rows are enough (the previous from which we're reading and the current one in which we're writting). At every iteration, we have to swap the row we're reading from/writting to. Because of that, the values are written in a zigzag shape between the rows 0 and 1.

This algorithm is good for the basic knacksack algorithm, in which only the value is stored in the table. In our case, we need to be careful because we are writting more than that. Meaning that we need to FIXME is it really the case? Or is there a bug in my code? FIXME what if the values are equal?





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
Call `hashcode.py` and pass the input data set as argument to solve the problem: `./hashcode.py path/to/data_set`.
The data to be submitted is in `STDOUT` and the score rewarded in `STDERR`.
Just redirect each file descriptor according to your needs.

Here is a loop to run the script for each data set.
```bash
$ mkdir -p output;
for f in data_sets/*; do \
    start=$SECONDS; \
    echo -n "${f}: "; \
    python hashcode.py $f > "output/$(basename $f .in).out"; \
    echo "in $(($SECONDS - $start)) seconds";
done
```
Here is the output (the files to submit are in the `output/` directory).
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

To run the unit tests, run `python -m unittest discover`.

## Improvements
* The score formula is pretty naive and doesn't prioritize the rides which must be finished early
* Instead of "just" taking the ride with the best score, some smart brute-force could be done
  * Bulding a graph and using a shortest path algorithm is probably a good solution
