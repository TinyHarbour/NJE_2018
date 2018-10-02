#!/usr/bin/env python3
#coding: utf-8

import requests
import sys
import os
from urllib.parse import urlencode, quote, urlsplit, parse_qsl
from scrapy.selector import Selector


# get http://www.pkulaw.cn/fulltext_form.aspx?Db=chl&Gid=73233
# or post http://www.pkulaw.cn/doGetFormatFullText.ashx

headers = {
        'Connection': 'keep-alive',
        'Origin': 'http://www.pkulaw.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'http://www.pkulaw.cn/fulltext_form.aspx?Gid=34732',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'click0=2018/10/1 15:36:56; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1538379201; ASP.NET_SessionId=0mopv3ubhn1givp33zvs4n3m; CookieId=0mopv3ubhn1givp33zvs4n3m; CheckIPAuto=0; CheckIPDate=2018-10-01 15:34:25; click1=2018/10/1 15:39:33; User_User=%b1%b1%be%a9%b4%f3%d1%a7; click2=2018/10/1 15:41:15; click3=2018/10/1 15:41:21; click4=2018/10/1 15:41:25; FWinCookie=0; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1538380799',
        }


def get_detail(gid):
    if not gid:
        raise Exception('gid empty')
    url = 'http://www.pkulaw.cn/doGetFormatFullText.ashx'
    params = {
            'Lib': 'chl',
            'Gid': gid,
            'IsUser': 'true',
            }
    data = urlencode(params)
    headers['Content-length'] = str(len(data))
    rsp = requests.post(url, data=params, headers=headers)
    s = Selector(text=rsp.text)
    fbm = s.css('#tbl_content_main tr:nth-child(2) a[href="/fbm"]::text').extract_first()
    content = s.css('#div_content').extract_first()
    if not fbm or not content:
        raise Exception('gid: %s rsp invalid: %, %s' % (gid, fbm, content))
    return fbm, content


def search(keyword):
    url = 'http://www.pkulaw.cn/doSearch.ashx'
    params = {
            'keyword': quote(keyword[-20:]),
            'range': 'name',
            'Search_Mode': 'accurate',
            'menu_item': 'law',
            'Db': 'chl',
            }
    data = urlencode(params)
    headers['Content-length'] = str(len(data))
    rsp = requests.post(url, data=params, headers=headers)
    s = Selector(text=rsp.text)
    href = s.css('#a_ft_1::attr(href)').extract_first()
    params = dict(parse_qsl(urlsplit(href).query))
    return params.get('Gid')


if __name__ == '__main__':
    gid = search(sys.argv[1])
    print(gid)
    print(get_detail(gid))
