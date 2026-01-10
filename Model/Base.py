from sqlalchemy.orm import DeclarativeBase
# 基类
class Base(DeclarativeBase):
    #可以放一些数据库表公共的字段,如id,created_at,updated_at等
    pass