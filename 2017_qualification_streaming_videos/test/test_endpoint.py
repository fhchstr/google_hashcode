import unittest

from hashcode.cacheserver import CacheServer
from hashcode.endpoint import Endpoint
from hashcode import Video

class TestEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint(0, 1000)
        # cache servers
        self.c0 = CacheServer(0, 100)
        self.c1 = CacheServer(1, 100)
        self.c2 = CacheServer(2, 100)
        self.e.latencies[self.c0] =  100
        self.e.latencies[self.c1] =  200
        self.e.latencies[self.c2] =  300

        # videos
        self.v0 = Video(0, 50)
        self.v1 = Video(1, 50)
        self.v2 = Video(2, 80)
        self.v3 = Video(3, 30)
        self.v4 = Video(4, 110)
        self.e.views[self.v3] = 1500
        self.e.views[self.v4] = 500
        self.e.views[self.v1] = 1000

    def test_time_saved(self):
        self.assertEqual(self.e.time_saved(self.v0, self.c0), 0)
        self.assertEqual(self.e.time_saved(self.v1, self.c0), 900000)  # (1000 - 100) * 1000
        self.assertEqual(self.e.time_saved(self.v1, self.c1), 800000)  # (1000 - 200) * 1000
        self.assertEqual(self.e.time_saved(self.v4, self.c2), 350000)  # (1000 - 300) * 500
