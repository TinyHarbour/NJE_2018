#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os

import mongo


if __name__ == '__main__':
    for item in mongo.find(status=0):
        line = '[%s](data/%s.md)\n' % (item['keyword'], item['gid'])
        f = open('../data/%s.md' % item['gid'], 'w')
        f.write(item['content'])
        f.close()
