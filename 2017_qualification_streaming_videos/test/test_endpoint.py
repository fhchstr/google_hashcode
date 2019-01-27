import unittest

from hashcode.cacheserver import CacheServer
from hashcode.endpoint import Endpoint
from hashcode.video import Video

class TestEndpoint(unittest.TestCase):

    def setUp(self):
        self.e = Endpoint(0, 1000)
        # cache servers
        self.c0 = CacheServer(0, 100)
        self.c1 = CacheServer(1, 100)
        self.c2 = CacheServer(2, 100)
        self.e.add_cache_server(self.c0, 100)
        self.e.add_cache_server(self.c1, 200)
        self.e.add_cache_server(self.c2, 300)

        # videos
        self.v0 = Video(0, 50)
        self.v1 = Video(1, 50)
        self.v2 = Video(2, 80)
        self.v3 = Video(3, 30)
        self.v4 = Video(4, 110)
        self.e.add_request_description(self.v3, 1500)
        self.e.add_request_description(self.v4, 500)
        self.e.add_request_description(self.v1, 1000)

    def test_add_cache_server(self):
        e = Endpoint(0, 1000)
        c0 = CacheServer(0, 100)
        c1 = CacheServer(1, 100)
        c2 = CacheServer(2, 100)

        e.add_cache_server(c0, 100)
        self.assertTrue(e.has_cache_server(c0))
        self.assertFalse(e.has_cache_server(c1))
        self.assertFalse(e.has_cache_server(c2))
        e.add_cache_server(c1, 200)
        self.assertTrue(e.has_cache_server(c0))
        self.assertTrue(e.has_cache_server(c1))
        self.assertFalse(e.has_cache_server(c2))
        e.add_cache_server(c2, 300)
        self.assertTrue(e.has_cache_server(c0))
        self.assertTrue(e.has_cache_server(c1))
        self.assertTrue(e.has_cache_server(c2))

    def test_add_request_description(self):
        e = Endpoint(0, 1000)
        v1 = Video(1, 50)
        v3 = Video(3, 30)
        v4 = Video(4, 110)

        e.add_request_description(v1, 1000)
        self.assertTrue(e.has_video(v1))
        self.assertFalse(e.has_video(v3))
        self.assertFalse(e.has_video(v4))
        e.add_request_description(v3, 1500)
        self.assertTrue(e.has_video(v1))
        self.assertTrue(e.has_video(v3))
        self.assertFalse(e.has_video(v4))
        e.add_request_description(v4, 500)
        self.assertTrue(e.has_video(v1))
        self.assertTrue(e.has_video(v3))
        self.assertTrue(e.has_video(v4))

    def test_time_saved(self):
        self.assertEqual(self.e.time_saved(self.v0, self.c0), 0)
        self.assertEqual(self.e.time_saved(self.v1, self.c0), 900000)  # (1000 - 100) * 1000
        self.assertEqual(self.e.time_saved(self.v1, self.c1), 800000)  # (1000 - 200) * 1000
        self.assertEqual(self.e.time_saved(self.v4, self.c2), 350000)  # (1000 - 300) * 500

    def test_latency(self):
        self.assertEqual(self.e.latency(self.c0), 100)
        self.assertEqual(self.e.latency(self.c1), 200)
        self.assertEqual(self.e.latency(self.c2), 300)

    def test_requests(self):
        self.assertEqual(self.e.requests(self.v0), 0)
        self.assertEqual(self.e.requests(self.v1), 1000)
        self.assertEqual(self.e.requests(self.v2), 0)
        self.assertEqual(self.e.requests(self.v3), 1500)
        self.assertEqual(self.e.requests(self.v4), 500)
