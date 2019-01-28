#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Author:  Fabien Hochstrasser
# Date:    2019-01-26
#
# Solve the Google Hash Code qualification 2017 challenge.
#
# Usage: hashcode.py path_to_data_set_file
#
import sys

from hashcode.cache import Cache
from hashcode.parser import Parser

def main(data_set):
    try:
        parser = Parser(data_set)
    except IOError as e:
        print('Cannot parse data-set: {}'.format(e))
        sys.exit(1)

    cache = Cache(parser.videos, parser.cache_servers, parser.endpoints)
    cache.distribute_videos()

    used_cache_servers = [c for c in cache.cache_servers if c.videos]
    print(len(used_cache_servers))
    for server in used_cache_servers:
        print('{} {}'.format(
            server.identifier,
            ' '.join([str(v.identifier) for v in server.videos])
        ))
    sys.stderr.write('{}\n'.format(score(cache)))

#    for server in cache.cache_servers:
#        print(server)
#        print(server.videos, sum([v.size for v in server.videos]))
#        print('')

def score(cache):
    """Return the score (average time saved per request, in microseconds) of the
    videos dispatching by the cache manager.
    """
    total_requests = 0
    time_saved = 0
    for endpoint in cache.endpoints:
        for video in endpoint.views:
            n_requests = endpoint.views[video]
            total_requests += n_requests
            time_saved += n_requests * (endpoint.data_center_latency - endpoint.latency_for_video(video))

    return int(time_saved / float(total_requests) * 1000)

if __name__ == '__main__':
    try:
        data_set = sys.argv[1]
    except (IndexError, IOError) as e:
        print('usage: {} path_to_data_set_file'.format(sys.argv[0]))
        sys.exit(1)

    main(data_set)
