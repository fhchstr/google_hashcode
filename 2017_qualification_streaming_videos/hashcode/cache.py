import math

class Cache(object):

    def __init__(self, videos, cache_servers, endpoints):
        self.videos = videos
        self.cache_servers = cache_servers
        self.endpoints = endpoints

    def distribute_videos(self):
        """Distribute the videos as efficiently as possible among the cache
           servers.
        """
        # FIXME We're not assigning the videos to the best cache here
        # FIXME see the (unefficient) code commented below to see what
        # FIXME should be done
        for cache_server in self.cache_servers:
            _, videos = self.best_videos_for_cache(cache_server)
            for video in videos:
                cache_server.add_video(video)
# Problem: Triangular number (X * (X + 1)) / 2 repetitions
#        cache_servers = set(self.cache_servers)
#
#        while(cache_servers):
#            best = (0, None, [])
#
#            for cache_server in cache_servers:
#                time_saved, videos = self.best_videos_for_cache(cache_server)
#                if time_saved > best[0]:
#                    best = time_saved, cache_server, videos
#
#            time_saved, cache_server, videos = best
#            if time_saved == 0:
#                break
#
#            for video in videos:
#                cache_server.add_video(video)
#
#            cache_servers.remove(cache_server)

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
                                   
                              m | 0 | 1 | 2 | 3 | 4 
                              --+---+---+---+---+---
                              0 | 0 | 0 | 0 | 0 | 0 
                              --+---+---+---+---+---
                        (v0)  1 | 0 | 0 | 2 | 2 | 2 
                              --+---+---+---+---+---
                        (v1)  2 | 0 | 0 | 2 | 2 | 4 
                              --+---+---+---+---+---
                        (v2)  3 | 0 | 0 | 2 | 3 | 4 

        FIXME Explain this step-by-step process better

        Column #1
        m(1, 1): v0 doesn't fit in capacity 1 -> m(0, 1) = 0
        m(2, 1): v1 doesn't fit in capacity 1 -> m(1, 1) = 0
        m(3, 1): v2 doesn't fit in capacity 1 -> m(2, 1) = 0

        Column #2
        m(1, 2): v0.value + m(0, 2-v0.size) = m(0, 0) = 2 + 0 = 2 we add it
        m(2, 2): v1.value + m(1, 2-v1.size) = m(1, 0) = 2 + 0 = 2 either one is good
        m(3, 2): v2 doesn't fit in capacity 2 -> m(2, 2) = 2

        Column #3
        m(1, 3): v0.value + m(0, 3-v0.size) = m(0, 1) = 2 + 0 = 2 we add it
        m(2, 3): v1.value + m(1, 3-v1.size) = m(1, 1) = 2 + 0 = 2 either one is good
        m(3, 3): v2.value + m(2, 3-v2.size) = m(2, 0) = 3 + 0 = 3

        Column #4
        m(1, 4): v0.value + m(0, 4-v0.size) = m(0, 2) = 2 + 0 = 2 we add it 
        m(2, 4): v1.value + m(1, 4-v1.size) = m(1, 2) = 2 + 2 = 4 we add it
        m(3, 4): v2.value + m(2, 4-v2.size) = m(2, 1) = 3 is smaller than m(2, 4)

        Args:
            cache_server: CacheServer instance which must be evaluated

        Return:
            the list of videos to store on the cache to save the most time
        """
        # Only look at the videos for which this cache can help saving time
        videos, time_saved = [], []
        for v in self.videos:
            t = cache_server.time_saved(v)
            if t > 0:
                videos.append(v)
                time_saved.append(t)

        # FIXME I tried to reduce the cache and video size by 10 to reduce
        # FIXME the running time. It helps, but that's not a clean solution
        div = 10.0 if cache_server.capacity >= 10 else 1.0

        # Build the evaluation table
        # FIXME it should be possible to allocate a much smaller table
        memo = [
            [(0, []) for capacity in xrange(int(cache_server.capacity / div) + 1)]
            for video in xrange(len(videos) + 1)
        ]

        for capacity in xrange(1, int(cache_server.capacity / div) + 1):
            for video_index_in_memo in xrange(1, len(videos) + 1):
                video = videos[video_index_in_memo-1]
                size = int(math.ceil(video.size / div))

                result_if_skipped = memo[video_index_in_memo-1][capacity]
                if size > capacity: 
                    # The video donesn't fit. Skip it and copy the value from the row
                    # above, which is the result we had before we evaluated this video.
                    # Since we skipped it, the result doesn't change.
                    memo[video_index_in_memo][capacity] = result_if_skipped
                    continue

                # The video fits. Find out what's best between skipping and adding it.
                # For code readability, retreive the best set of videos (and time saved
                # by caching them) for capacity = capacity - video.size
                best_for_smaller_capacity = memo[video_index_in_memo-1][capacity-size]
                best_time_saved, best_videos = best_for_smaller_capacity

                result_if_added = (
                    best_time_saved + time_saved[video_index_in_memo-1],
                    best_videos + [video],
                )

                memo[video_index_in_memo][capacity] = max(
                    result_if_added,
                    result_if_skipped,
                )

        # The best result is in the bottom right corner
        return memo[-1][-1]
