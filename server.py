#! /usr/bin/env python
# coding=utf8
from email import message
import time
from concurrent import futures

import grpc

from rpc.example import example_pb2_grpc,example_pb2
from internal.core import etcd_server


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class TestService(example_pb2_grpc.GreeterServicer):
    '''
    继承GrpcServiceServicer,实现hello方法
    '''
    def __init__(self):
        pass

    def SayHello(self, request, context):
        '''
        具体实现hello的方法,并按照pb的返回对象构造HelloResponse返回
        :param request:
        :param context:
        :return:
        '''
        result =  request.name + " : this is gprc test service"
        return example_pb2.HelloReply(message = result)

def run():
    service_name = "gmsec.srv.pytest"
    server_addr = "localhost:82" # '[::]:50052'
    etcd_server.StartService(service_name,server_addr)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_GreeterServicer_to_server(TestService(),server)
    server.add_insecure_port(server_addr)
    server.start()
    print("start service...",server_addr)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()