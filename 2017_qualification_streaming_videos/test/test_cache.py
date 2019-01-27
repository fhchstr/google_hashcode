import os
import unittest

from hashcode.cache import Cache
from hashcode.parser import Parser


TEST_INPUT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_simple.in')

class TestCache(unittest.TestCase):

    def setUp(self):
        parser = Parser(TEST_INPUT)
        self.cache = Cache(parser.videos, parser.cache_servers, parser.endpoints)

    def test_best_videos(self):
        time_saved, videos = self.cache.best_videos_for_cache(self.cache.cache_servers[0])
        self.assertEqual(time_saved, 4)
        self.assertEqual(videos, self.cache.videos[:2])
