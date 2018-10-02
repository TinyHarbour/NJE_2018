#!/usr/bin/env python3
#coding: utf-8


import sys
import re

import crawl
import mongo


def do(keyword):
    try:
        gid = crawl.search(keyword)
        fbm, content = crawl.get_detail(gid) 
        mongo.insert(gid, keyword=keyword, fbm=fbm, content=content, status=0)
    except:
        mongo.insert(0, keyword=keyword, status=1)


if __name__ == '__main__':
    for line in sys.stdin:
        do(line.strip())
