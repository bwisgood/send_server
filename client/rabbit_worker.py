import pika, json
import sys

sys.path.append('../')
from client.send_client import FuncObj

import socket
import fcntl
import struct


# def get_ip_address(ifname):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
#
#
# try:
#     ifname = 'eth0'.encode()
#     if_address = get_ip_address(ifname)
# except Exception:
#     if_address = '0.0.0.0'

username = 'guest'  # 指定远程rabbitmq的用户名密码
pwd = 'guest'
# if if_address == "172.17.121.248":
#     print(if_address)
#     pwd = '12345'

user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', credentials=user_pwd))  # 创建连接
chan = s_conn.channel()  # 在连接上创建一个频道

chan.queue_declare(queue='balance')  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行


def callback(ch, method, properties, body):  # 定义一个回调函数，用来接收生产者发送的消息
    data = json.loads(body.decode())
    func_name = data.pop("func_name")
    func = FuncObj().__getattribute__(func_name)
    func(**data)
    print(data)


chan.basic_consume(on_message_callback=callback,  # 调用回调函数，从队列里取消息
                   queue='balance',  # 指定取消息的队列名
                   auto_ack=True)  # 取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
print('[消费者] waiting for msg .')
chan.start_consuming()  # 开始循环取消息
