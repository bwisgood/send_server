from models import Base
from sqlalchemy import Column, Integer, String, Enum, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# 生成orm基类
from datetime import datetime


class BaseModel(object):
    add_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    add_user = Column(String(30), nullable=False)
    update_user = Column(String(30), nullable=True)
    is_delete = Column(Integer, nullable=False, default=0)


class TaskBaseModel(BaseModel):
    """任务表（任务基本表）"""
    # 任务名称
    name = Column(String(255))
    # 任务内容
    content = Column(Text)
    # 执行频率
    rate = Column(String(255), nullable=True)
    # 紧急程度
    exigent_degree = Column(Enum('日常', '普通', '紧急', '非常紧急'), default="日常")
    # 任务职能(站岗: 中控)
    task_function = Column(Enum('自定义', '检查', '清洁', "巡逻", '站岗', '绿化', '联系', '检修'), default='自定义')
    # 截止时间
    end_time = Column(DateTime, nullable=True)
    # 开始时间
    start_time = Column(DateTime, nullable=True)
    # 权重
    weight = Column(Integer, default=1)


class Task(Base, TaskBaseModel):
    '''任务表'''
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    # 任务状态
    status = Column(Enum('未完成', '已完成', '已逾期', '逾期完成'), default="未完成")
    # 是否有子任务
    has_tasks = Column(Integer)
    # 计划执行岗位
    executor_plan = Column(Integer, ForeignKey("position.id", ondelete="SET NULL"), nullable=True)
    # 临时执行岗位
    executor_temporary = Column(Integer, ForeignKey("position.id", ondelete="SET NULL"), nullable=True)
    # 小区id
    community_id = Column(Integer, ForeignKey("community.id"))


class Emergency(Base, BaseModel):
    __tablename__ = "emergency"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    thinking = Column(String(500), nullable=False)
    status = Column(Enum('未处理', '已处理'), default='未处理')
    position = Column(String(255))


class Repair(Base, BaseModel):
    """
    维修单
    """

    __tablename__ = "repair"

    id = Column(Integer, primary_key=True)
    # 损坏情况
    situation = Column(Text)
    # 报修地点
    address = Column(String(100))
    # add_time 保修时间 add_user 保修人


class TaskRecords(Base):
    """任务记录表"""
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True)

    executor_department = Column(Integer, ForeignKey("department.id", ondelete="SET NULL"), nullable=True)
    weight = Column(Integer, )


class TaskRecordsPosition(Base):
    '''任务记录-岗位中间表'''
    __tablename__ = "taskrecords_position"
    id = Column(Integer, primary_key=True)
    task_records_id = Column(Integer)
    position_id = Column(Integer)
    plan_temporary = Column(Integer, comment='0plan 1temporary')
    is_leader = Column(Integer, comment='0不是 1是')
