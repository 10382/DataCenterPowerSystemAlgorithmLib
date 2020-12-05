# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

import grpc
import redis
import pandas as pd
from proto import powerpredict_pb2, powerpredict_pb2_grpc
from concurrent import futures
from utils import redis_utils, preprocess
from algorithm import pred

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PowerPredictService(powerpredict_pb2_grpc.PowerPredictServiceServicer):

    def PowerPredict(self, request, context):
        print("服务端接收到用户请求："+request.host)
        # 根据请求的start和end以及数据库的数据存储间隔进行请求的划分
        # 服务器相关的请求
        redis_req_list = redis_utils.redis_ts_split(request.start, request.end, request.host)
        # PDU 相关的请求
        pdu_req_list = redis_utils.redis_ts_split(request.start, request.end, "pdu-mini")
        # Redis 连接配置
        redis_pool = redis.ConnectionPool(host="localhost", port=6379, password="lidata429")
        # 建立连接
        r = redis.Redis(connection_pool=redis_pool)
        # 请求数据并转datafrme
        server_df = preprocess.req2df(redis_req_list, r, request.start, request.end)
        pdu_df = preprocess.req2df(pdu_req_list, r, request.start, request.end)
        # 缺失值填充
        preprocess.fillna_decompose(server_df)
        # 异常值处理
        preprocess.outlier_decompose(server_df)
        # 归一化
        minmax_np = preprocess.minmax(server_df)
        print(minmax_np.shape)
        minmax_np = preprocess.pred_concat(minmax_np)
        print(minmax_np.shape)
        # pred.rf_train(minmax_np, pdu_df.values[:minmax_np.shape[0]])
        y_pred = pred.rf_test(minmax_np)
        # return powerpredict_pb2.PowerPredictReply(power='The power of %s is %s !' % (request.host, y_pred[0]))
        return powerpredict_pb2.PowerPredictReply(power='%s' % (y_pred[0]))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    powerpredict_pb2_grpc.add_PowerPredictServiceServicer_to_server(PowerPredictService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
