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
    for server in cache.cache_servers:
        print(server)
        print(server.videos)
        print('')

if __name__ == '__main__':
    try:
        data_set = sys.argv[1]
    except (IndexError, IOError) as e:
        print('usage: {} path_to_data_set_file'.format(sys.argv[0]))
        sys.exit(1)

    main(data_set)
