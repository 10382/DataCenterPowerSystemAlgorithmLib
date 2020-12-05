# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

import grpc
from concurrent import futures
from proto import powerevaluate_pb2, powerevaluate_pb2_grpc

if __name__ == "__main__":
    channel = grpc.insecure_channel("localhost:50052")
    stub = powerevaluate_pb2_grpc.PowerEvaluateServiceStub(channel)

    res = stub.PowerEvaluate(powerevaluate_pb2.PowerEvaluateRequest(host="compute01", targetTimestamp="1568294222"))
    print(res)
