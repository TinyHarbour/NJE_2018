#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

client = MongoClient().test.law # collection

#schema
# gid: str, gid
# keyword: law title
# content: crawl from pkulaw.cn
# status: 0 suc, 1 fail
# add more fields


def find(**kwargs):
    return client.find(kwargs)


def insert(gid, keyword, **kwargs):
    data = kwargs
    data['gid'] = gid
    data['keyword'] = keyword
    if client.find_one({'gid': gid, 'keyword': keyword}):
        return client.update({'gid': gid, 'keyword': keyword}, data)
    else:
        return client.insert(data)


def stat():
    return client.count()


if __name__ == '__main__':
   print(stat())
