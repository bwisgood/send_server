from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from .task_models import *
#
engine = create_engine(
    # r'mysql+pymysql://root:mysql@192.168.1.155:3306/ai_community_v3.1',
    # encoding='utf-8')
# engine = create_engine(
#     r'mysql+pymysql://root:mysql@127.0.0.1:3306/ai_community_v3',
#     encoding='utf-8')
# engine = create_engine(
    r'mysql+pymysql://root:Yuanjia2018@rm-2ze33fuactgx09184oo.mysql.rds.aliyuncs.com:3306/ai_community_v4',
    encoding='utf-8')

Base = declarative_base()


class DBSession(object):
    has_init = False

    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.has_init:
            self.session = sessionmaker(bind=engine)()
            self.has_init = True


def get_session():
    # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    # Session_class = sessionmaker(bind=engine)
    # session = Session_class()  # 生成session实例
    session = DBSession().session
    return session
