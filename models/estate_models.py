from models import Base
from sqlalchemy import Column, Integer, String, Enum, Float, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

# 生成orm基类
from datetime import datetime


class Area(Base):
    """
    区域
    """

    __tablename__ = "area"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    community_id = Column(Integer, ForeignKey("community.id"))

    buildings = relationship("Building", backref="area", lazy="dynamic")


class Building(Base):
    """
    楼房表
    """

    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    area_id = Column(Integer, ForeignKey("area.id"))

    units = relationship("Unit", backref="building", lazy="dynamic")


class Unit(Base):
    """
    单元表
    """

    __tablename__ = "unit"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    building_id = Column(Integer, ForeignKey("building.id"))

    rooms = relationship("Room", backref="unit", lazy="dynamic")



class Room(Base):
    """
    房间表
    """

    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    full_name = Column(String(255))
    # 面积
    square = Column(Integer)
    public_square = Column(Integer, default=0)
    room_state = Column(Enum("已出售", "未出售"), default="未出售")
    # 因为有多对多关系 所以需要加入参数判断谁是业主
    owner_id = Column(Integer)
    # 备注
    remark = Column(Text)
    # 如果没有微信 则直接保存业主基本信息
    owner_name = Column(String(255))
    owner_mobile = Column(String(255))
    owner_id_card = Column(String(255))

    unit_id = Column(Integer, ForeignKey("unit.id"))

    bills = relationship("Bill", backref="room")


class EstateCategory(Base):
    """
    物业资产分类
    """

    __tablename__ = "estate_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    community_id = Column(Integer, ForeignKey("community.id", ondelete="CASCADE"))
    # 级联删除所有物品
    sub_category = relationship("EstateSubCategory", backref="estate_category", cascade='all, delete-orphan')


class EstateSubCategory(Base):
    """
    物业资产子分类
    """

    __tablename__ = "estate_sub_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    parent_id = Column(Integer, ForeignKey("estate_category.id", ondelete="CASCADE"))


class Estate(Base):
    """
    物业资产
    """
    __tablename__ = "estate"
    id = Column(Integer, primary_key=True)
    no = Column(String(255))
    name = Column(String(255))
    position = Column(String(255), nullable=True)
    # 经度
    longtitude = Column(Float, nullable=True)
    # 维度
    latitude = Column(Float, nullable=True)
    qr_code = Column(String(255))
    category = Column(String(255))

    community_id = Column(Integer, ForeignKey("community.id"))
