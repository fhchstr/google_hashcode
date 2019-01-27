import bisect


class Endpoint(object):

    def __init__(self, identifier, data_center_latency):
        self.identifier = identifier
        self.data_center_latency = data_center_latency

        self.cache_servers = {}
        self.cache_servers_sorted_by_latency = []
        self.videos = {}
        self.videos_sorted_by_views = []

    def add_cache_server(self, cache_server, latency):
        cache_server.add_endpoint(self)
        bisect.insort_left(self.cache_servers_sorted_by_latency, (latency, cache_server))
        self.cache_servers[cache_server.identifier] = {
            'ref': cache_server,
            'latency': latency,
        }

    def add_request_description(self, video, n_requests):
        bisect.insort_left(self.videos_sorted_by_views, (n_requests, video))
        self.videos[video.identifier] = {
            'ref': video,
            'n_requests': n_requests,
        }

    def has_cache_server(self, cache_server):
        """Return True if this endpoint is connected to this cache server."""
        return cache_server.identifier in self.cache_servers

    def has_video(self, video):
        """Return True if this endpoint watches this video."""
        return video.identifier in self.videos

    def time_saved(self, video, cache_server):
        """Return the time saved if this video is hosted on this cache server."""
        n_requests = self.requests(video)
        if n_requests == 0 or self.video_already_on_better_cache(video, cache_server):
            return 0

        time_saved_per_request = self.data_center_latency - self.latency(cache_server)
        return time_saved_per_request * n_requests

    def video_already_on_better_cache(self, video, cache_server):
        """Return True if the video is already hosted on a better cache.

        A cache is better if it has a smaller or the same latency.
        """
        latency_limit = self.latency(cache_server)
        for (latency, other_cache) in self.cache_servers_sorted_by_latency:
            if latency > latency_limit:
                break
            if other_cache.has_video(video):
                return True

        return False
        
    def latency(self, cache_server):
        """Return the latency from this endpoint to the cache server."""
#        try:
        return self.cache_servers[cache_server.identifier]['latency']
#        except KeyError:
#            raise RuntimeError('endpoint not connected to cache server, cannot compute latency')

    def requests(self, video):
        """Return the number of requests made for this video."""
        if video.identifier not in self.videos:
            return 0

        return self.videos[video.identifier]['n_requests']
