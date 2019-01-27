from cacheserver import CacheServer
from endpoint import Endpoint
from video import Video


class Parser(object):
    """Parse the input data set and instate the entities defined.

    The parsing is inefficient because the file is read multiple times. Once for
    each section. I focused on the code readability instead of efficiency for this
    part, as it is for sure not the one in which most time will be spent.
    """
    def __init__(self, data_set):
        self._data_set = data_set

        sizes = self._parse_sizes()
        n_endpoints = sizes[1]
        n_cache_servers = sizes[3]
        cache_server_capacity = sizes[4]

        self.cache_servers = [
            CacheServer(i, cache_server_capacity)
            for i in xrange(n_cache_servers)
        ]
        self.videos = self._parse_videos()
        self.endpoints = [e for e in self._parse_endpoints(n_endpoints)]
        self._parse_requests()

    def _parse_sizes(self):
        """Parse the size of the entities.
    
        The first line of the input contains the following numbers:
          - the number of videos
          - the number of endpoints
          - the number of request descriptions
          - the number of cache servers
          - the capacity of each cache server in megabytes
    
        Returns:
            a tuple of the values read, in the order above
        """
        with open(self._data_set, 'r') as f:
            # First line
            return tuple([int(v) for v in f.readline().split()])


    def _parse_videos(self):
        """Parse the videos.
    
        The 2nd line contains the sizes of individual videos in megabytes.
    
        Returns:
            a list of videos.
        """
        with open(self._data_set, 'r') as f:
            f.readline()  # skip the 1st line
            return [
                Video(i, int(size))
                for i, size in enumerate(f.readline().split())
            ]

    def _parse_endpoints(self, n):
        """Parse the endpoints.
    
        The endpoints section starts after the first 2 lines. It describes each of
        the endpoints one after another. The description of each endpoint consists
        of the following lines:
            - a line containing tow numbers
                - the latency of serving a video request from the data center to
                  this endpoint, in milliseconds
                - the number of cache servers that this endpoint is connected to
            - X lines describing the connections from the endpoint to each of the
              X connected cache servers. Each line contains the following numbers:
                - the ID of the cache server
                - the latency of serving a video request from this cache server to
                  this endpoint, in milliseconds

        Args:
            n: the number of endpoints to parse

        Returns:
            a generator over the Endpoint objects instantiated
        """
        with open(self._data_set, 'r') as f:
            f.readline()  # skip the 1st line
            f.readline()  # skip the 2nd line
            for i in xrange(n):
                data_center_latency, n_cache_servers = [int(v) for v in f.readline().split()]
                endpoint = Endpoint(i, data_center_latency)
                for _ in xrange(n_cache_servers):
                    id_, latency = [int(v) for v in f.readline().split()]
                    endpoint.add_cache_server(self.cache_servers[id_], latency)

                yield endpoint
                n -= 1

    def _parse_requests(self):
        """
        Finally, the last section contains the request descriptions in separate lines.
        Each line contains the following numbers:
            - the ID of the requested video
            - the ID of the endpoint from which the requests are coming from
            - the number of requests
        """
        with open(self._data_set, 'r') as f:
            f.readline()  # skip the 1st line
            f.readline()  # skip the 2nd line
            for line in f:
                values = [int(v) for v in line.split()]
                # The request descriptions  are the only lines with 3 elements per line.
                # So we can just skip all the lines with a different number of elements.
                if len(values) != 3:
                    continue

                video = self.videos[values[0]]
                endpoint = self.endpoints[values[1]]
                n_requests = values[2]

                endpoint.add_request_description(video, n_requests)
