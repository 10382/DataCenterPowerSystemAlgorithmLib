# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

import grpc
from concurrent import futures
from proto import powerpredict_pb2, powerpredict_pb2_grpc

if __name__ == "__main__":
    channel = grpc.insecure_channel("localhost:50051")
    stub = powerpredict_pb2_grpc.PowerPredictServiceStub(channel)

    res = stub.PowerPredict(powerpredict_pb2.PowerPredictRequest(host="compute01", start="1568297400", end="1568297409"))
    print(res)
