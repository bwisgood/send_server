#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import grpc
import json
from send_server_util import send_server_pb2, send_server_pb2_grpc

_HOST = '0.0.0.0'
# _HOST = '39.106.101.198'
_PORT = '19998'


class FuncObj():
    def sen_message_test(self, ):
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            message = "{name} 您好，关于您物业费账单{no}：{money}元 还未支付，请您尽快支付，" \
                      "物业：{phone} 北京市元甲律师事务所： 张旭 13811945816。您可登录微信小程序{mp_name}进行在线支付"
            response = client.SendMessage(send_server_pb2.SendMessageParam(user_id=102, message=message))
        print("received: " + str(response))

    def debt_remind_test(self, user_id=None, bill_id=None):
        """账单欠款通知"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "账单欠款通知"
            if not all((user_id, bill_id)):
                bill_id = 30
                user_id = 102
            page_path = ''
            id_json = json.dumps({"bill_id": bill_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))

    def repair_remind_test(self, user_id=None, repair_id=None):
        """新报修通知"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "新报修通知"
            if not all((user_id, repair_id)):
                repair_id = 22
                user_id = 102
            page_path = ''
            id_json = json.dumps({"repair_id": repair_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))

    def emergency_remind_test(self, user_id=None, emergency_id=None):
        """应急情况处理通知"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "物业管理通知"
            if not all((user_id, emergency_id)):
                emergency_id = 2
                user_id = 102
            page_path = ''
            id_json = json.dumps({"emergency_id": emergency_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))

    def work_remind_test(self, user_id=None, task_id=None):
        """任务提醒通知"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "物业管理通知"
            if not all((user_id, task_id)):
                task_id = 20
                user_id = 102
            page_path = ''
            id_json = json.dumps({"task_id": task_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))

    def feedback_remind_test(self, user_id=None, community_feedback_id=None):
        """意见反馈提醒"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "意见反馈提醒"
            if not all((user_id , community_feedback_id)):
                user_id = 102
                community_feedback_id = 1
            page_path = ''
            id_json = json.dumps({"community_feedback_id": community_feedback_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))

    def vote_remind_test(self,user_id,vote_id):
        """物业电子投票通知"""
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            template_id = "物业电子投票通知"
            if not all((user_id , vote_id)):
                user_id = 102
                vote_id = 1
            page_path = ''
            id_json = json.dumps({"vote_id": vote_id})
            response = client.SendTemplateMessage(
                send_server_pb2.SendTemplateMessageParam(user_id=user_id, template_id=template_id, page_path=page_path,
                                                         id_json=id_json))
        print("received: " + str(response))



    def get_perform(self, bill_id):
        """获取律师函"""
        if not bill_id:
            bill_id = 5
        with grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT)) as channel:
            client = send_server_pb2_grpc.SendServiceStub(channel=channel)
            response = client.GetLawyerletter(send_server_pb2.GetLawyerLetterParam(bill_id=bill_id))
        print("received: " + str(response))


if __name__ == '__main__':



    fun_obj = FuncObj()
    fun_obj.get_perform(3)
    # fun_obj.sen_message_test()
    fun_obj.debt_remind_test()
    fun_obj.repair_remind_test()
    fun_obj.emergency_remind_test()
    fun_obj.work_remind_test()
    fun_obj.feedback_remind_test()
    # channel = grpc.insecure_channel("{0}:{1}".format(_HOST, _PORT))
    # client = send_server_pb2_grpc.GreeterStub(channel=channel)
    # response = client.SayHello(models_pb2.HelloRequest(name='you', message='hey guys'))
    # print("received: " + response.message)
