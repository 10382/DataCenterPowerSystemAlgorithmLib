# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from utils import redis_utils
from sklearn.preprocessing import MinMaxScaler

# 根据请求的 key 值列表去数据库取数据拼接，并做切片，返回DataFrame
def req2df(req_list, r, start=None, end=None):
    for i, req in enumerate(req_list):
        get_dict = r.hgetall(req)
        get_dict = redis_utils.redis2dict(get_dict)
        if i == 0:
            if start == end:
                df = pd.DataFrame(get_dict, index=[start])
            else:
                df = pd.DataFrame(get_dict)
        else:
            df = pd.concat([df, pd.DataFrame(get_dict)])
        if start != None and end != None:
            df = df.loc[start: end, :]
    return df

# 虚拟机分解模块需要用到的
def req_vm2df(req, r, targetTs):
    vm_list = redis_utils.redis_set2list(r.smembers(req + ".virtualMachineSet"))
    req_vm_list = list(map(lambda x: x+'.'+targetTs, vm_list))
    vm_df_list = []
    for req_vm in req_vm_list:
        vm_df_list.append(req2df([req_vm], r, targetTs, targetTs))
    return vm_df_list

# 缺失值填充
def fillna_decompose(df, value=None, columns=None, methods="zero"):
    if columns == None:
        columns = df.columns.values
    if value != None:
        df[columns] = df[columns].fillna(value)
    else:
        if methods == "zero":
            df[columns] = df[columns].fillna(0)
        else:
            pass	# 待完工

# 异常值处理
def outlier_decompose(df, columns=None, types="nonega", upbounds=None):
    if columns == None:
        columns = df.columns.values
    df[df[columns] < 0] = 0
    if types == "nonega":
        return
    if isinstance(upbounds, list):
        for i in range(len(columns)):
            df[df[[columns[i]]] > upbounds[i]] = upbounds[i]
    else:
        df[df[columns] > upbounds] = upbounds


# 最大最小归一化
def minmax(data, minmax_range=None):
    scaler = MinMaxScaler()
    if minmax_range == None:
        return scaler.fit_transform(data)
    else:
        scaler.fit(minmax_range)
        return scaler.transform(data)

# 预测数据格式转换
def pred_concat(data, time_len=10, overlap=True):
    data_new = data
    for i in range(1, time_len):
        data_new = np.concatenate((data_new, np.roll(data, -1, axis=0)), axis=1)
    return data_new[:-(time_len-1)]
