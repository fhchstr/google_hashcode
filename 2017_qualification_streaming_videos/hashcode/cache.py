import math

# FIXME Rename to CacheManager
class Cache(object):

    def __init__(self, videos, cache_servers, endpoints):
        self.videos = videos
        self.cache_servers = cache_servers
        self.endpoints = endpoints

    def distribute_videos(self):
        """Distribute the videos as efficiently as possible among the cache
           servers.

        The cache servers with the best potential latency gain are evaluated first.
        """
        # FIXME use this or not?
        video_avg_size = sum(v.size for v in self.videos) / len(self.videos)

        for cache_server in sorted(
            self.cache_servers,
            key=lambda s: s.potential_latency_gain(),
            reverse=True
        ):
            _, videos = self.xxx(cache_server)
            print videos
#            _, videos = self.best_videos_for_cache(cache_server)
            cache_server.videos = videos

    def best_videos_for_cache(self, cache_server):
        """Return the most efficient (=bigger time saved) set of videos that can
           be stored on the cache server.

        There is no silver bullet to find the best set, all the possibilities
        must be evaluated. For each video, the algorithm must decide if it is:
            - included in the set (time saved goes up, capacity goes down)
            - not included in the set (time saved and capacity remain the same)
        Once all the possibilities have been evaluated, the best one is returned.

        Let's say we have 3 videos and a cache capacity of 4:
            - v0(size=2, time_saved=2)
            - v1(size=2, time_saved=2)
            - v2(size=3, time_saved=3)

        The  obvious solution for this simple data set is to store v0 and v1 to
        have a total time saved of 4. The algorithm uses a modifed version of
        the knapsack algorithm: https://en.wikipedia.org/wiki/Knapsack_problem.

        The idea of the algorithm is to build a bottom-up table which keeps track of
        the highest value for the items which can be included without going above the
        maximum capacity. Because it's bottom-up, the algorithm looks first at how
        much value can fit when the capacity is small (=1) and then continues until
        it evaluated the value which can fit in the actual capacity.

        The only difference with the original knapsack algorithm, is that instead
        of just keeping track of the highest value (=time saved), the algorithm also
        keeps track of which videos were included in the set to get this result.

        Here is how the knapsack algorithm works:
          - create a table of (1 + #videos) rows and (1 + capacity) columns filled
            with zeroes. Rows represent videos, columns represent remaining capacity.
            Some of the columns are not realistic depending on the input data set.
            With the example above, remaining capacity can never be 3 because there
            is no video of size=1 in the data set. But it's easier to compute those
            non-realistic cases than checking if they're realistic or not...

          - traverse the table column-by-column from the top left corner, skipping
            the row and column 0 (effectively starting at index (1, 1)).

          - For each cell:
            NOTE: the row indexes are shifted by 1 because the table has 1 + #videos
                  rows. So the video of line i is actually videos[i-1]

              - Don't include the video if it doesn't fit in the remaining capacity.
                If the video isn't included, the value and remaining capacity remain
                the same. So just copy the value from the row above which corresponds
                to the value after including (or not) the previous video.

              - If the video fits in the remaining capacity, it can either be
                included in the set, or not. So evaluate both scenarios and store the
                best result.

        Given the example above, here is how the resulting table looks like. The best
        value is the one in the bottom right cell. For simplicity, the tracking of
        the videos isn't represented on the table.

                     table m    | 0 | 1 | 2 | 3 | 4
                              --+---+---+---+---+---
                              0 | 0 | 0 | 0 | 0 | 0
                              --+---+---+---+---+---
                        (v0)  1 | 0 | 0 | 2 | 2 | 2
                              --+---+---+---+---+---
                        (v1)  2 | 0 | 0 | 2 | 2 | 4
                              --+---+---+---+---+---
                        (v2)  3 | 0 | 0 | 2 | 3 | 4

        Here is the step-by-step explanation of the algorithm used to fill the table.
        The coordinates are written as m(row, column), the best choice is marked with
        an asterisk at the end of the line.

        FIXME explain what happens if the score is the same.

        Column #1
        m(1, 1): v0 doesn't fit in capacity 1 -> m(0, 1) = 0 (skip*)
        m(2, 1): v1 doesn't fit in capacity 1 -> m(1, 1) = 0 (skip*)
        m(3, 1): v2 doesn't fit in capacity 1 -> m(2, 1) = 0 (skip*)

        Column #2
        m(1, 2): v0 fits it capacity 2. Find the max between:
            - m(0, 2) = 0                                                 (skip)
            - v0.value + m(0, 2-v0.size) = v0.value + m(0, 0) = 2 + 0 = 2 (add*)
        m(2, 2): v1 fits in capacity 2. Find the max between:
            - m(1, 2) = 2                                                 (skip*) FIXME
            - v1.value + m(1, 2-v0.size) = v1.value + m(1, 0) = 2 + 0 = 2 (add*)  FIXME
        m(3, 2): v2 doesn't fit in capacity 2 -> m(2, 2) = 2 (skip*)

        Column #3
        m(1, 3): v0 fits in capacity 3. Find the max between:
            - m(0, 3) = 0                                                 (skip)
            - v0.value + m(0, 3-v0.size) = v0.value + m(0, 1) = 2 + 0 = 2 (add*)
        m(2, 3): v1 fits in capacity 3. Find the max between:
            - m(1, 3) = 2                                                 (skip*) FIXME
            - v1.value + m(1, 3-v1.size) = v1.value + m(1, 1) = 2 + 0 = 2 (add*)  FIXME
        m(3, 3): v2 fits in capacity 3. Find the max between:
            - m(2, 3) = 2                                                 (skip)
            - v2.value + m(2, 3-v2.size) = v2.value + m(2, 0) = 3 + 0 = 3 (add*)

        Column #4
        m(1, 4): v0 fits in capacity 4. Find the max between:
            - m(0, 4) = 0                                                 (skip)
            - v0.value + m(0, 4-v0.size) = v0.value + m(0, 2) = 2 + 0 = 2 (add*)
        m(2, 4): v1 fits in capacity 4. Find the max between:
            - m(1, 4) = 2                                                 (skip)
            - v1.value + m(1, 4-v1.size) = v1.value + m(1, 2) = 2 + 2 = 4 (add*)
        m(3, 4): v2 fits in capcity 4. Find the max between:
            - m(2, 4) = 4                                                 (skip*)
            - v2.value + m(2, 4-v2.size) = v2.value + m(2, 1) = 3 + 0     (add)

        As you might have noticed, only the previous row (index-1) is used to
        compute the values of the next row. This means we don't need to allocate
        #videos rows. 2 rows are enough (the previous from which we're reading and
        the current one in which we're writting). At every iteration, we have to
        swap the row we're reading from/writting to. Because of that, the values
        are written in a zigzag shape between the rows 0 and 1.

        This algorithm is good for the basic knacksack algorithm, in which only the
        value is stored in the table. In our case, we need to be careful because we
        are writting more than that. Meaning that we need to 
        FIXME is it really the case? Or is there a bug in my code?
        FIXME what if the values are equal?
        
        Args:
            cache_server: CacheServer instance which must be evaluated

        Return:
            the list of videos to store on the cache to save the most time
        """
        # Only look at the videos for which this cache can help saving time
        videos_and_time_saved = []
        for v in self.videos:
            t = cache_server.time_saved(v)
            if t > 0:
                videos_and_time_saved.append((v, t))

        memo = [
            [(0, set()) for capacity in xrange(cache_server.capacity + 1)]
            for _ in range(2)
        ]

        for capacity in xrange(1, cache_server.capacity + 1):
            for video_index_in_memo in xrange(1, len(videos_and_time_saved) + 1):
                # Alternate the current row for each video
                current_row = video_index_in_memo % 2
                previous_row = (video_index_in_memo - 1) % 2

                video, time_saved = videos_and_time_saved[video_index_in_memo-1]
                result_if_skipped = memo[previous_row][capacity]

                if video.size > capacity:
                    # The video donesn't fit. Skip it and copy the value from the
                    # other row, which is the result we had before we evaluated this
                    # video. Since we skipped it, the result doesn't change.
                    memo[current_row][capacity] = result_if_skipped
                    continue

                # The video fits. Find out what's best between skipping and adding it.
                # For code readability, retreive the best set of videos (and time saved
                # by caching them) for capacity = capacity - video.size
                best_for_smaller_capacity = memo[previous_row][capacity - video.size]
                best_time_saved, best_videos = best_for_smaller_capacity

                # FIXME is this check really necessary? I think so because of the
                # FIXME 2-rows solution
                if video in best_videos:
                    memo[current_row][capacity] = result_if_skipped
                    continue

                result_if_added = (
                    best_time_saved + time_saved,
                    best_videos | set([video]),
                )

                memo[current_row][capacity] = max(
                    result_if_added,
                    result_if_skipped,
                )

        # The best result is in the last cell of the last row visited
        return memo[current_row][-1]


    def knapsack(sefl, cache_server, videos_and_time_saved, videos):
        capacity = cache_server.capacity - sum(v.size for v in videos)

        memo = [
            [(0, set()) for cap in xrange(capacity + 1)]
            for _ in range(2)
        ]

        for capacity in xrange(1, capacity + 1):
            for video_index_in_memo in xrange(len(videos), len(videos_and_time_saved) - len(videos) + 1):
                # Alternate the current row for each video
                current_row = video_index_in_memo % 2
                previous_row = (video_index_in_memo - 1) % 2

                video, time_saved = videos_and_time_saved[video_index_in_memo-1]
                result_if_skipped = memo[previous_row][capacity]

                if video.size > capacity:
                    # The video donesn't fit. Skip it and copy the value from the
                    # other row, which is the result we had before we evaluated this
                    # video. Since we skipped it, the result doesn't change.
                    memo[current_row][capacity] = result_if_skipped
                    continue

                # The video fits. Find out what's best between skipping and adding it.
                # For code readability, retreive the best set of videos (and time saved
                # by caching them) for capacity = capacity - video.size
                best_for_smaller_capacity = memo[previous_row][capacity - video.size]
                best_time_saved, best_videos = best_for_smaller_capacity

                # FIXME is this check really necessary? I think so because of the
                # FIXME 2-rows solution
                if video in best_videos:
                    memo[current_row][capacity] = result_if_skipped
                    continue

                result_if_added = (
                    best_time_saved + time_saved,
                    best_videos | set([video]),
                )

                memo[current_row][capacity] = max(
                    result_if_added,
                    result_if_skipped,
                )

        # The best result is in the last cell of the last row visited
        return memo[current_row][-1]





    def xxx(self, cache_server):
        """
            sort the video by ratio
            put the X first videos, until the capacity used reached some threshold
            this threshold can be calculated with the avg size of the videos in the set
        """
        # Only look at the videos for which this cache can help saving time
        videos_and_time_saved = []
        for video in self.videos:
            time_saved = cache_server.time_saved(video)
            if time_saved > 0:
                videos_and_time_saved.append((video, time_saved))
        # Sort them by time_saved/size ratio, the goal is to process first the ones
        # with the best ratio
        videos_and_time_saved = sorted(
            videos_and_time_saved,
            key=lambda vt: vt[1] / vt[0].size,
            reverse=True
        )

        videos = []

        for i, (video, time_saved) in enumerate(videos_and_time_saved):
            if video.size + sum(v.size for v in videos) > cache_server.capacity:
                break
            videos.append(video)

        return None, videos
#        return self.knapsack(cache_server, videos_and_time_saved, videos)
