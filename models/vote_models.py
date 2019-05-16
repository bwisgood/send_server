from models import Base
from sqlalchemy import Column, Integer, String, Enum, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# 生成orm基类
from datetime import datetime


class Vote(Base):
    '''投票模型'''

    __tablename__ = "vote"
    id = Column(Integer, primary_key=True)
    # 小区
    community_id = Column(Integer)
    # 标题
    title = Column(String(255))
    # 投票内容
    content = Column(String(255))
    # 开始时间
    start_time = Column(DateTime)
    # 截止时间
    end_time = Column(DateTime)
    # 状态
    status = Column(String(255), comment='未开始 进行中 已结束', default='未开始')
    # 总人数
    total_user = Column(Integer, default=0)
    # 总面积
    total_area = Column(Float, default=0.0)
    # 同意人数
    agree_user = Column(Integer, default=0)
    # 同意面积
    agree_area = Column(Float, default=0.0)
    # 反对人数
    against_user = Column(Integer, default=0)
    # 反对面积
    against_area = Column(Float, default=0.0)
