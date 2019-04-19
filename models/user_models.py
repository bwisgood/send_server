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


class User(Base):
    '''用户表'''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    # 昵称
    nickname = Column(String(255), nullable=False)
    # 用户名称
    name = Column(String(255), nullable=True)
    # 小程序openid
    openid = Column(String(255))
    # 用户ｕｎｉｏｎｉｄ
    unionid = Column(String(255), nullable=True)
    # 用户手机号
    mobile = Column(String(255), nullable=True)
    # 小区ｉｄ
    community_id = Column(Integer, ForeignKey("community.id"))


class MPUser(Base):
    """
    微信公众号用户
    """
    __tablename__ = "mp_user"

    id = Column(Integer, primary_key=True)
    # 0是已关注 1是未关注
    subscribe = Column(Integer, default=0)
    # openid
    openid = Column(String(255), nullable=False)
    # unionid
    unionid = Column(String(255))
    # 小区外键
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)


class Company(Base):
    """
    公司表
    """

    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    # 手机号用mobile 固话用phone
    phone = Column(String(255), nullable=True)
    # 公众号的app id和app secret
    mp_app_id = Column(String(255))
    mp_app_secret = Column(String(255))
    # 开放平台
    open_app_id = Column(String(255))
    open_app_secret = Column(String(255))

    # 微信开放平台的账号信息
    key = Column(String(255), nullable=True)
    communities = relationship("Community", backref="company")


class Community(Base):
    """
    小区id
    """

    __tablename__ = "community"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    phone = Column(String(255))

    # 小程序的app_id和app_secret
    app_id = Column(String(255))
    app_secret = Column(String(255))
    address = Column(String(255))
    # 微信商户平台的账号
    mch_id = Column(String(255), nullable=True)
    mch_key = Column(String(255), nullable=True)
    key = Column(String(255), nullable=True)

    free_latter = Column(Integer, default=50)
    latter_price = Column(Integer, default=5000)
    proprietor_show = Column(Integer, default=1)
    company_id = Column(Integer, ForeignKey("company.id"))
    task_popover = Column(Integer)


class Department(Base):
    """
    部门表
    """

    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    community_id = Column(Integer, ForeignKey("community.id"))


class Position(Base):
    """
    岗位表
    """

    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    department_id = Column(Integer, ForeignKey("department.id", ondelete="CASCADE"))


class CommunityFeedback(Base, BaseModel):
    '''小区反馈表'''

    __tablename__ = "community_feedback"
    id = Column(Integer, primary_key=True)
    community_id = Column(Integer, ForeignKey("community.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(255))
    content = Column(Text)

    status = Column(Integer, comment='0未解决　1正在处理　2已解决')
