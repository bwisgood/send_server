from models.user_models import Position, User,Community
from models.bill_models import Bill
from models.estate_models import Room
from send_server_util.doc_utils import DocReplace
from datetime import datetime
import os
from models.task_models import TaskRecords, TaskRecordsPosition
from models import get_session

session = get_session()
bill_id = 3
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
else:

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
# users = session.query(User).filter(User.community_id == 1,
#                                    Position.user_id == User.id
#                                    ).all()
# positions = session.query(Position).filter(User.community_id == 1,
#                                            Position.user_id == User.id
#                                            ).all()
# data = {}
# for user in users:
#     position_ids = [position.id for position in session.query(Position).filter(Position.user_id == user.id).all()]
#     weight_list = [task_records.weight for task_records in session.query(TaskRecords).filter(
#         TaskRecords.id == TaskRecordsPosition.task_records_id,
#         TaskRecordsPosition.position_id.in_(position_ids)
#     ).all()]
#     print(weight_list)
#     data[user.id] = sum(weight_list)
#
# data_dic = {}
# for po in positions:
#     data_dic[(po.id, po.name)] = data.get(po.user_id)
#     print(data.get(po.user_id))
# print(data_dic)
