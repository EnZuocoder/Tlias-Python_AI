from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from Model.Base import Base
#学生模型类
class StudentModel(Base):
    __tablename__ = "student"  # 数据库表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(20),nullable=False)
    no:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    gender:Mapped[int] = mapped_column(Integer,nullable=False)
    phone:Mapped[str] = mapped_column(String(20),nullable=False)
    idCard:Mapped[str] = mapped_column(String(50),nullable=False,unique=True,name="id_card")
    isCollege:Mapped[int] = mapped_column(Integer,nullable=False,name="is_college")
    degree:Mapped[int] = mapped_column(Integer)
    address:Mapped[str] = mapped_column(String(200))
    clazzId:Mapped[int] = mapped_column(Integer,name="clazz_id")
    graduationDate:Mapped[datetime] = mapped_column(DateTime,name="graduation_date")
    # 违纪次数和违纪分数
    violationCount:Mapped[int] = mapped_column(Integer,default=0,name="violation_count")
    violationScore:Mapped[int] = mapped_column(Integer,default=0,name="violation_score")
    createTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(),name="create_time")
    updateTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),name="update_time")