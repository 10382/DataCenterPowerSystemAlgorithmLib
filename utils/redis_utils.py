# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys
import json
import redis

# 将redis中的hash数据取出并转为dict
def redis2dict(in_dict):
    return dict(zip(map(bytes.decode, in_dict.keys()), map(json.loads, in_dict.values())))

# 将redis中的set数据取出并转为list
def redis_set2list(in_set):
    print(in_set)
    return list(map(bytes.decode, in_set))

def redis_ts_split(start, end, hostname, interval=100):
    start = int(start)
    end = int(end)
    new_start = (start // interval) * interval
    new_end = (end // interval + 1) * interval - 1
    req_list = []
    for ts_start in range(new_start // interval, (new_end + 1) // interval):
        req_list.append("%s.%d.%d" % (hostname, ts_start * interval, (ts_start * interval + interval - 1)))
    print(req_list)
    return req_list
