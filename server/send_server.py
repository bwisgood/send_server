import grpc
import requests
import time
import json
import redis

import os
import sys
sys.path.append('../')
# sys.path.append('/root/send_server')

from concurrent import futures
from datetime import datetime

from server.constants import RET
from send_server_util import send_server_pb2_grpc
from send_server_util import send_server_pb2
from send_server_util.doc_utils import DocReplace
from models import get_session
from models.user_models import User, Position, Department, CommunityFeedback, MPUser
from models.user_models import Community
from models.user_models import Company
from models.bill_models import Bill, AmountBill
from models.estate_models import Room
from models.task_models import Task, Emergency, Repair

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = "0.0.0.0"
_PORT = "19999"
REDIS_HOST = '0.0.0.0'
REDIS_PORT = 6379
redis_cli = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


class WxUtils(object):
    def __init__(self, app_id, app_secret, company_id):
        self.app_id = app_id
        self.app_secret = app_secret
        self.company_id = company_id

    def get_access_token(self):
        company_id = self.company_id
        access_token = redis_cli.get("mp_access_token_{}".format(company_id))
        if access_token and access_token != 'None':
            return access_token

        request_url = "https://api.weixin.qq.com/cgi-bin/token"
        payload = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }

        response = requests.get(url=request_url, params=payload)
        if response.status_code != 200:
            return None

        response_data = response.json()

        access_token = response_data.get("access_token")
        if access_token:
            return None

        redis_cli.setex("mp_access_token_{}".format(company_id), 7100, str(access_token))

        return access_token if access_token else None


class TemplateData:
    template_id_func_dict = {
        # 物业费缴费提醒
        "-Qk6HzmI9NseDlZ6D_AGhVdA7IBZYQ8b0m6muUlkAF4": "finance_remid",
        # 物业管理通知
        "hVmPaXBnI-C4_lzduy4jsM1Te33lcuiz6jWzvNwsCG8": "work_remind",
        # 物业账单通知
        "ODPeSmbLTwIjA25Rft0NfVcNLrt6LDMVqZLD5i4khr8": "bill_remind",
        # 新报修通知
        "iRIoLPbosbaQ6ExqyVJ6COGawoIGQ_r29cElxAox6wU": "repair_remind",
        # 账单欠款通知
        "xvIb4DxhBDzZcmd746cdo6LOncy4c7JQto7zQLt-L5w": "debt_remind",
        # 商品发货通知
        "-AJSXplHwCNlDY4Je3sYY0P_HYfkebuUbRkxOs3s4vo": "goods_send_remind",
        # 推荐成功通知
        "C5dqZvacTVrdMXUyKngjdhf6Dop15NsSFUugovnY6VQ": "recommend_remind",
        # 订阅课程开课提醒
        "GAxhLJmFux4Y-4MICMe6jx0NKQ38tSFzISAYFoQDTaA": "class_begin_remind",
        # 意见反馈提醒
        "Qe4K360d6zczLePcZoIvgIMsUPewlYZE4tMP5t3ROnU": "feedback_remind",
    }

    def get_data(self, template_id, **kwargs):
        func_name = self.template_id_func_dict.get(template_id)
        func = self.__getattribute__(func_name)
        session = get_session()
        data = func(session, **kwargs)
        return data

    def feedback_remind(self, session, community_feedback_id):
        """
        社区反馈通知
        :param community_feedback_id: 反馈ｉｄ
        :return:
        """
        """{{first.DATA}}
        提出人：{{keyword1.DATA}}
        时间：{{keyword2.DATA}}
        住址：{{keyword3.DATA}}
        内容：{{keyword4.DATA}}
        {{remark.DATA}}"""
        try:
            add_user_name, add_time, room_name, content = session.query(
                User.name, CommunityFeedback.add_time, Room.full_name, CommunityFeedback.content
            ).filter(
                CommunityFeedback.id == community_feedback_id,
                User.id == CommunityFeedback.add_user,
                Room.owner_name == User.name,
            ).first()
        except:
            return {}

        data = {
            "first": "您好！您的管理区域内有客户提出意见反馈！",
            "keyword1": {
                "value": add_user_name,
            },
            "keyword2": {
                "value": add_time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "keyword3": {
                "value": room_name,
            },
            "keyword4": {
                "value": content,
            },
            "remark": {
                "value": "请尽快处理回复客户的意见反馈。",
            },
        }

        return data

    def deal_feedback(self, session, community_feedback_id):
        """
        反馈处理通知
        :param community_feedback_id: 反馈ｉｄ
        :return:
        """
        """{{first.DATA}}
        相关房屋：{{keyword1.DATA}}
        反馈类型：{{keyword2.DATA}}
        反馈状态：{{keyword3.DATA}}
        反馈信息：{{keyword4.DATA}}
        工作人员：{{keyword5.DATA}}
        {{remark.DATA}}"""
        pass

    def recommend_remind(self, session, user_id):
        """
        推荐成功通知
        :param user_id: 推荐用户ｉｄ
        :return:
        """
        """{{first.DATA}}
        微信昵称：{{keyword1.DATA}}
        时间：{{keyword2.DATA}}
        {{remark.DATA}"""

    def class_begin_remind(self, session, class_id):
        """
        订阅课程开课提醒
        :param class_id: 课程id
        :return:
        """
        """{{first.DATA}}
        课程标题：{{keyword1.DATA}}
        课程内容：{{keyword2.DATA}}
        主讲老师：{{keyword3.DATA}}
        时间：{{keyword4.DATA}}
        {{remark.DATA}}"""

    def debt_remind(self, session, bill_id):
        """
        账单欠款通知
        :param bill_id: 账单ｉｄ
        :return:
        """
        """{{first.DATA}}
        住户姓名：{{keyword1.DATA}}
        物业单元：{{keyword2.DATA}}
        账单周期：{{keyword3.DATA}}
        账单总额：{{keyword4.DATA}}
        欠款金额：{{keyword5.DATA}}
        {{remark.DATA}}"""
        try:
            user_name, room_name, bill_frequency, bill_sum = session.query(
                Bill.user_name, Room.full_name, AmountBill.frequency, Bill.sum
            ).filter(
                Bill.id == bill_id,
                Room.id == Bill.room_id,
                Bill.amount_bill_id == AmountBill.id
            ).first()
        except Exception as e:
            print(e)
            return {}
        data_dict = {
            "first": "物业缴费提醒",
            "keyword1": {
                "value": user_name,
            },
            "keyword2": {
                "value": room_name,
            },
            "keyword3": {
                "value": bill_frequency,
            },
            "keyword4": {
                "value": bill_sum,
            },
            "keyword5": {
                "value": bill_sum,
            },
            "remark": {
                "value": "请尽快缴费",
            },

        }
        return data_dict

    def goods_send_remind(self, session, bill_id):
        """
        商品发货通知
        :param bill_id: 账单ｉｄ
        :return:
        """
        """{{first.DATA}}
        订单金额：{{keyword1.DATA}}
        商品明细：{{keyword2.DATA}}
        收货地址：{{keyword3.DATA}}
        订单编号：{{keyword4.DATA}}
        送货人及单号：{{keyword5.DATA}}
        {{remark.DATA}}"""
        pass

    def work_remind(self, session, task_id=None, emergency_id=None):
        """
        工作提醒
        :param task_id: 任务ｉｄ
        :return:
        """
        """{{first.DATA}}
        标题：{{keyword1.DATA}}
        发布时间：{{keyword2.DATA}}
        内容：{{keyword3.DATA}}
        {{remark.DATA}}"""
        if task_id:
            try:
                user_name, task_title, update_time, task_content = session.query(
                    User.name, Task.name, Task.update_time, Task.content
                ).filter(
                    Task.id == Task.id,
                    Task.executor_plan == Position.id,
                    Position.user_id == User.id
                ).first()
                first = "辛勤的{},你好".format(user_name)
                remark = "请尽快执行"
            except:
                return {}
        elif emergency_id:
            try:
                user_name, task_title, update_time, task_content = session.query(
                    User.name, Emergency.title, Emergency.add_time, Emergency.thinking
                ).filter(
                    Emergency.id == emergency_id,
                    Emergency.add_user == User.id
                ).first()
                first = "尊敬的{}管理员,有紧急情况待处理".format(user_name)
                remark = "请尽快登录物业后台处理"
            except:
                return {}
        else:
            return {}
        data = {
            "first": {
                "value": first
            },
            "keyword1": {
                "value": task_title,
            },
            "keyword2": {
                "value": update_time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "keyword3": {
                "value": task_content,
            },
            "remark": {
                "value": remark,
            },
        }
        return data

    def finance_remind(self, session, bill_id):
        """
        账单提醒
        :param bill_id: 账单ｉｄ
        :return:
        """
        """{{first.DATA}}
        业主姓名：{{userName.DATA}}
        地址：{{address.DATA}}
        物业费金额：{{pay.DATA}}
        {{remark.DATA}}
        """
        pass

    def bill_remind(self, session, bill_id):
        """
        物业账单通知
        :param bill_id: 账单ｉｄ
        :return:
        """
        """{{first.DATA}}
        截止日期：{{keyword1.DATA}}
        房间号：{{keyword2.DATA}}
        物业号：{{keyword3.DATA}}
        已欠物业服务费：{{keyword4.DATA}}
        {{remark.DATA}}"""
        pass

    def repair_remind(self, session, repair_id):
        """
        报修提醒
        :param repair_id: 报修单ｉｄ
        :return:
        """
        """{{first.DATA}}
        联系人：{{keyword1.DATA}}
        电话：{{keyword2.DATA}}
        房号：{{keyword3.DATA}}
        报修内容：{{keyword4.DATA}}
        报修时间：{{keyword5.DATA}}
        {{remark.DATA}}"""
        try:
            user_name, mobile, repair_content, repair_addr, repair_time = session.query(
                User.name, User.mobile, Repair.situation, Repair.address, Repair.add_time
            ).filter(
                Repair.id == repair_id,
                User.id == Repair.add_user,
            ).first()
        except:
            return {}
        data = {
            "first": "新报修通知",
            "keyword1": {
                "value": user_name,
            },
            "keyword2": {
                "value": mobile,
            },
            "keyword3": {
                "value": repair_addr,
            },
            "keyword4": {
                "value": repair_content,
            },
            "keyword5": {
                "value": repair_time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "remark": "请尽快联系客户。",
        }
        return data


class SendServer(send_server_pb2_grpc.SendServiceServicer):
    """服务类"""

    def SendMessage(self, request, context):
        # 发送短信
        user_id = request.user_id
        print(type(user_id))
        if not (request.user_id and request.message):
            return send_server_pb2.SendMessageResponse(msg='缺少用户ｉｄ或发送的消息', code=int(RET.PARAMERR), data='')
        print(str(request))
        session = get_session()
        try:
            user, community = session.query(User, Community).filter(User.id == user_id,
                                                                    Community.id == User.community_id).first()
        except Exception as e:
            print(e)
            return send_server_pb2.SendMessageResponse(msg='00000', code=int(RET.NODATA), data='')
        if not user:
            return send_server_pb2.SendMessageResponse(msg='未查询到该用户', code=int(RET.NODATA), data='')
        if not community:
            return send_server_pb2.SendMessageResponse(msg='未查询到该用户的小区', code=int(RET.NODATA), data='')
        mobile = user.mobile
        # community_mobile = community.phone
        send_message = request.message
        sms_url = "http://data.yuanjia101.com/API/Sys/SMS"
        # temp_data = {
        #     "name": user.name,
        #     "no": '123121e3dwds',
        #     "money": 131311,
        #     "phone": community_mobile,
        #     "mp_name": community.name
        # }
        request_data = {
            "title": '交钱',
            "mobile": mobile,
            "content": send_message
            # "content": send_message.format(**temp_data)
        }
        resp = requests.post(sms_url, data=request_data)
        if int(resp.json().get("err")) == 0:
            return send_server_pb2.SendMessageResponse(msg='发送成功', code=int(RET.OK), data='')
        return send_server_pb2.SendMessageResponse(msg='发送失败', code=int(RET.SERVERERR), data='')

    def get_template_data(self, template_id, **kwargs):
        # 获取要发送的信息的数据
        template_data_getter = TemplateData()
        data = template_data_getter.get_data(template_id, **kwargs)
        return data

    def SendTemplateMessage(self, request, context):
        print("request: " + str(request))
        # 发送模板消息
        # 用户ｉｄ
        user_id = request.user_id
        # 模板消息ｉｄ
        template_id = request.template_id
        page_path = request.page_path
        session = get_session()
        # 获取公司id ，服务号appid，app_secret
        company_id, mp_app_id, mp_app_secret = session.query(
            Company.id, Company.mp_app_id, Company.mp_app_secret
        ).filter(User.id == user_id, Community.id == User.community_id,
                 Company.id == Community.company_id).first()
        # 获取access_token
        try:
            community_app_id, openid = session.query(
                Community.app_id, MPUser.openid
            ).filter(
                User.id == user_id,
                Community.id == User.community_id,
                User.unionid == MPUser.unionid
            ).first()
        except:
            return send_server_pb2.SendTemplateMessageResponse(code=int(RET.PARAMERR), msg='用户不存在或未关注该公司的公众号', data='')

        wx_utils = WxUtils(mp_app_id, mp_app_secret, company_id)
        access_token = wx_utils.get_access_token()
        id_dict = json.loads(request.id_json)
        # 获取要发送的信息的数据
        template_data = self.get_template_data(template_id, **id_dict)
        if not template_data:
            send_server_pb2.SendTemplateMessageResponse(code=int(RET.PARAMERR), msg='查询错误', data='')
        miniprogram = {
            'appid': community_app_id,
            # 要跳转的小程序页面
            'pagepath': page_path,
        }
        # 组织数据
        data = {
            'touser': openid,
            'miniprogram': miniprogram,
            'data': template_data,
            'template_id': template_id
        }
        url_send = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(
            access_token)
        headers = {'Content-Type': 'application/json'}
        # 发送模板消息
        data = json.dumps(data)
        send_resp = requests.post(url=url_send, data=data, headers=headers).content.decode()
        resp_dict = json.loads(send_resp)
        if resp_dict.get("errmsg") != "ok":
            errmsg = resp_dict.get("errmsg")
            errmsg = "发送失败"
            code = RET.SERVERERR
            print("发送失败")
        else:
            code = RET.OK
            errmsg = "发送成功"
            print("发送成功")
        return send_server_pb2.SendTemplateMessageResponse(code=int(code), msg=errmsg, data='')

    def GetLawyerletter(self, request, context):
        # 生成律师函
        bill_id = request.bill_id
        session = get_session()
        try:
            user_name, room_name, add_time, sum, address, phone = session.query(
                Bill.user_name, Room.full_name, Bill.add_time, Bill.sum, Community.address, Community.phone
            ).filter(
                Bill.id == bill_id,
                Room.id == Bill.room_id,
                Community.id == Bill.community_id,
            ).first()
        except Exception as e:
            print(e)
            return send_server_pb2.GetLawyerLetterRespnse()
        now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        base = os.path.dirname(os.path.dirname(__file__))
        filename = "".join([user_name or "N", now, str(bill_id), ".docx"])
        temp_path = base + "/static/律师函.docx"
        to_path = base + "/static/generated/{}".format(filename)
        d = DocReplace(temp_path, to_path)
        context = {
            "name": user_name,
            "room_full_name": room_name,
            "add_time": datetime.strftime(add_time, "%Y年%m月%d日"),
            "now": datetime.strftime(datetime.now(), "%Y年%m月%d日"),
            "sum": str(sum / 100),
            "lawyer_contact": "188888888",
            "pay_address": address,
            "pay_phone": phone,
            "address": "北京市朝阳区建外SOHO东区B座703室"
        }
        print(context)
        d.replace(context)
        print("request: " + str(request))
        return send_server_pb2.GetLawyerLetterRespnse()


def server():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    send_server_pb2_grpc.add_SendServiceServicer_to_server(SendServer(), grpcServer)
    grpcServer.add_insecure_port("{0}:{1}".format(_HOST, _PORT))
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    server()
