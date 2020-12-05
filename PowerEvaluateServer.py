# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

import grpc
import redis
import pandas as pd
from proto import powerevaluate_pb2, powerevaluate_pb2_grpc
from concurrent import futures
from utils import redis_utils, preprocess
from algorithm import pred

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PowerEvaluateService(powerevaluate_pb2_grpc.PowerEvaluateServiceServicer):

    def PowerEvaluate(self, request, context):
        print("服务端接收到用户请求："+request.host)
        # Redis 连接配置
        redis_pool = redis.ConnectionPool(host="localhost", port=6379, password="lidata429", db=1)
        # 建立连接
        r = redis.Redis(connection_pool=redis_pool)
        # 请求数据并转datafrme
        vm_fea_list = preprocess.req_vm2df(request.host + '.' + request.targetTimestamp, r, request.targetTimestamp))
#        server_df, vm_df_list = preprocess.req2df(redis_req_list, r, request.start, request.end)
#        pdu_df = preprocess.req2df(pdu_req_list, r, request.start, request.end)
#        # 缺失值填充
#        preprocess.fillna_decompose(server_df)
#        # 异常值处理
#        preprocess.outlier_decompose(server_df)
#        # 归一化
#        minmax_np = preprocess.minmax(server_df)
#        print(minmax_np.shape)
#        minmax_np = preprocess.pred_concat(minmax_np)
#        print(minmax_np.shape)
#        # pred.rf_train(minmax_np, pdu_df.values[:minmax_np.shape[0]])
#        y_pred = pred.rf_test(minmax_np)
#        # return powerpredict_pb2.PowerPredictReply(power='The power of %s is %s !' % (request.host, y_pred[0]))
        return powerevaluate_pb2.PowerEvaluateReply(power='%s' % ("123"))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    powerevaluate_pb2_grpc.add_PowerEvaluateServiceServicer_to_server(PowerEvaluateService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
