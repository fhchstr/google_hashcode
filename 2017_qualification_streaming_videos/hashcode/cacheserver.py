class CacheServer(object):

    def __init__(self, identifier, capacity):
        self.identifier = identifier
        self.capacity = capacity

        self.endpoints = []
        self.videos = set()

    def time_saved(self, video):
        """Return the cumulative time saved, among all the endpoints, if the
        video is hosted on this cache_server.
        """
        return sum([e.time_saved(video, self) for e in self.endpoints])

    def potential_latency_gain(self):
        """Return the total number of milliseconds potentially saved if the videos
           watched by the connected endpoints are all hosted on this cache server.
        """
        gain = 0
        for endpoint in self.endpoints:
            n_requests = sum(endpoint.views.values())
            gain += n_requests * (endpoint.data_center_latency - endpoint.latencies[self])
        return gain

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join([
                'identifier={}'.format(self.identifier),
                'capacity={}'.format(self.capacity),
            ])
        )
