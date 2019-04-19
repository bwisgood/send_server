from models import Base
from sqlalchemy import Column, Integer, String, Enum, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# 生成orm基类
from datetime import datetime


class BillType(Base):
    """
    账单类型表
    """
    __tablename__ = "bill_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    community_id = Column(Integer, ForeignKey("community.id"))


class Bill(Base):
    """
    账单表
    """

    __tablename__ = "bill"

    id = Column(Integer, primary_key=True)
    sum = Column(Integer)
    no = Column(String(255))
    # 业主姓名
    user_name = Column(String(255), nullable=True)
    room_id = Column(Integer, ForeignKey("room.id"))
    status = Column(Enum("已支付", "未支付"), default="未支付")
    urgency_times = Column(Integer, default=0)
    bill_type = Column(String(255))
    add_time = Column(DateTime, default=datetime.now)
    finish_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    title = Column(String(255))
    remark = Column(String(255))
    community_id = Column(Integer, ForeignKey("community.id"))
    amount_bill_id = Column(Integer, ForeignKey("amount_bill.id"))


class UrgencyMethod(Base):
    """
    催收方式表
    """

    __tablename__ = "urgency_method"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Urgency(Base):
    """
    催收表
    """

    __tablename__ = "urgency"

    id = Column(Integer, primary_key=True)
    method = Column(String(255))
    add_time = Column(DateTime, default=datetime.now)

    bill_id = Column(Integer, ForeignKey("bill.id"))


class UrgencyIncome(Base):
    """
    催收收入表
    """

    __tablename__ = "urgency_income"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bill.id"))
    status = Column(Enum("未支付", "已支付"), default="未支付")
    sum = Column(Integer)
    add_time = Column(DateTime, default=datetime.now)
    finish_time = Column(DateTime, default=datetime.now)
    no = Column(String(255))
    add_admin = Column(Integer)


class AmountBill(Base):
    """
    账单总表
    """

    __tablename__ = "amount_bill"

    id = Column(Integer, primary_key=True)
    frequency = Column(Enum("月", "季度", "年", "一次性"), default="一次性")
