import bisect


class Endpoint(object):

    def __init__(self, identifier, data_center_latency):
        self.identifier = identifier
        self.data_center_latency = data_center_latency

        self.latencies = {}
        self.views = {}

    def time_saved(self, video, cache_server):
        """Return the time saved if this video is hosted on this cache server."""
        if video not in self.views or self.video_already_on_better_cache(video, cache_server):
            return 0

        time_saved_per_view = self.data_center_latency - self.latencies[cache_server]
        return time_saved_per_view * self.views[video]

    def video_already_on_better_cache(self, video, cache_server):
        """Return True if the video is already hosted on a better cache.

        A cache is better if it has a smaller or the same latency.
        """
        for other_cache in self.latencies:
            if other_cache is cache_server:
                continue
            if (
                self.latencies[other_cache] <= self.latencies[cache_server]
                and video in other_cache.videos
            ):
                return True

        return False

    def latency_for_video(self, video):
        """Return the latency for a video.

        If the video is on 1-n cache server connected to this endpoint, the
        latency of the best one is returned. If the video is not on any cache
        server, the latency of the data center is returned.
        """
        latency = self.data_center_latency
        for cache_server in self.latencies:
            if video in cache_server.videos:
                if self.latencies[cache_server] < latency:
                    latency = self.latencies[cache_server]

        return latency
