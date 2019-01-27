class CacheServer(object):

    def __init__(self, identifier, capacity):
        self.identifier = identifier
        self.capacity = capacity

        self.used_space = 0
        self.endpoints = []
        self.videos = {}

    def add_endpoint(self, endpoint):
        self.endpoints.append(endpoint)

    def add_video(self, video):
        """Add this video on the cache server."""
        if self.used_space + video.size > self.capacity:
            msg = '{v} too big for {c} (capacity={c.capacity}, used space={c.used_space}'
            raise RuntimeError(msg.format(v=video, c=self))

        self.videos[video.identifier] = video

    def has_video(self, video):
        """Return true if this video is on the cache server."""
        return video.identifier in self.videos

    def time_saved(self, video):
        """Return the cumulative time saved, among all the endpoints, if the
        video is hosted on this cache_server.
        """
        return sum([e.time_saved(video, self) for e in self.endpoints])

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join([
                'identifier={}'.format(self.identifier),
                'capacity={}'.format(self.capacity),
            ])
        )
