import os
import unittest

from hashcode.parser import Parser

TEST_INPUT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.in')

class TestParser(unittest.TestCase):

    def setUp(self):
        self.p = Parser(TEST_INPUT)

    def test_cache_servers(self):
        self.assertEqual(len(self.p.cache_servers), 3)
        self.assertEqual({c.capacity for c in self.p.cache_servers}, set([100]))

        self.assertEqual(self.p.cache_servers[0].identifier, 0)
        self.assertEqual(self.p.cache_servers[-1].identifier, len(self.p.cache_servers) - 1)

    def test_videos(self):
        self.assertEqual(len(self.p.videos), 5)
        self.assertEqual(self.p.videos[0].size, 50)
        self.assertEqual(self.p.videos[1].size, 50)
        self.assertEqual(self.p.videos[2].size, 80)
        self.assertEqual(self.p.videos[3].size, 30)
        self.assertEqual(self.p.videos[4].size, 110)

        self.assertEqual(self.p.videos[0].identifier, 0)
        self.assertEqual(self.p.videos[-1].identifier, len(self.p.videos) - 1)

    def test_endpoints(self):
        self.assertEqual(len(self.p.endpoints), 2)
        self.assertEqual(self.p.endpoints[0].identifier, 0)
        self.assertEqual(self.p.endpoints[0].data_center_latency, 1000)
        self.assertEqual(self.p.endpoints[1].identifier, 1)
        self.assertEqual(self.p.endpoints[1].data_center_latency, 500)

        self.assertTrue(self.p.cache_servers[0] in self.p.endpoints[0].latencies)
        self.assertTrue(self.p.cache_servers[1] in self.p.endpoints[0].latencies)
        self.assertTrue(self.p.cache_servers[2] in self.p.endpoints[0].latencies)
        self.assertFalse(self.p.cache_servers[0] in self.p.endpoints[1].latencies)
        self.assertFalse(self.p.cache_servers[1] in self.p.endpoints[1].latencies)
        self.assertFalse(self.p.cache_servers[2] in self.p.endpoints[1].latencies)

        self.assertFalse(self.p.videos[0] in self.p.endpoints[0].views)
        self.assertTrue(self.p.videos[1] in self.p.endpoints[0].views)
        self.assertFalse(self.p.videos[2] in self.p.endpoints[0].views)
        self.assertTrue(self.p.videos[3] in self.p.endpoints[0].views)
        self.assertTrue(self.p.videos[4] in self.p.endpoints[0].views)
        self.assertTrue(self.p.videos[0] in self.p.endpoints[1].views)
        self.assertFalse(self.p.videos[1] in self.p.endpoints[1].views)
        self.assertFalse(self.p.videos[2] in self.p.endpoints[1].views)
        self.assertFalse(self.p.videos[3] in self.p.endpoints[1].views)
        self.assertFalse(self.p.videos[4] in self.p.endpoints[1].views)
