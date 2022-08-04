"""
客户端,用于发现服务。
"""
from asyncio.windows_events import NULL
import time
import json
import sched
import queue
import threading

import random
import grpc
import etcd3
import requests
from flask import Flask, jsonify

app = Flask(__name__)

service_name =  "gmsec.srv.pytest"
# etcd 连接对象
client = etcd3.client(host="192.155.1.121", port=30400)  # etcd默认的启动配置

# g_queue = queue.Queue()
# g_server_list = []

# 获取服务名字列表
def GetConn(serviceName):
    list = GetServerList(serviceName)
    if len(list) > 0:
        item = random.choice(list)
        return grpc.insecure_channel(item["Addr"])
    return None

# 获取服务名字列表
def GetServerList(serviceName):
    path = serviceName
    result = client.get_prefix(path)
    out = []
    ip_port_list = [ip.decode() for ip, _ in result]
    offset = int(time.time()) - (10*60*60)
    for ip in ip_port_list:
        tmp = json.loads(ip)
        if tmp["Metadata"] > offset:
            out.append(tmp)
    return out


def watch_callback(event):
    # 这里event 还不会用,我直接获取全部
    GetServerList(service_name)


def find_all_server():
    # ---------- 获取启动的服务器数据---------------------------
    GetServerList(service_name)
    # 监听gmsec.service变化,有变化触发watch_callback,其实就是重新触发set_g_server_list
    client.add_watch_prefix_callback(service_name, watch_callback)


@app.route("/")
def client_views():
    server_ip = ""
    try:
        server_ip = g_queue.get(timeout=0.2)
        print("send -->", server_ip)

        res = requests.get("http://" + server_ip, timeout=2)
        print("res", res.text)
        g_queue.put(server_ip)
    except Exception as e:
        print("error -> ", e)
        if server_ip and server_ip in g_server_list:
            g_queue.put(server_ip)
        return jsonify({"code": 1, "msg": e.__str__()})
    return jsonify(json.loads(res.text))


if __name__ == '__main__':
    # something_schedule()
    find_all_server()
    app.run(host="127.0.0.1", port=5000)
