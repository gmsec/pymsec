#! /usr/bin/env python
# coding=utf8

import grpc
from rpc import example

from rpc.example import example_pb2_grpc,example_pb2
from internal.core import etcd_client
service_name = "gmsec.srv.pytest"

def run():
    '''
    模拟请求服务方法信息
    :return:
    '''
    conn=etcd_client.GetConn(service_name) # grpc.insecure_channel('localhost:50052')
    client = example_pb2_grpc.GreeterStub(channel=conn)
    request = example_pb2.HelloRequest(name="xiao gang")
    respnse = client.SayHello(request)
    print("received:",respnse.message)


if __name__ == '__main__':
    run()
