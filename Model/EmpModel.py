from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from Model.Base import Base
# 员工模型类
class EmpModel(Base):
    __tablename__ = "emp"  # 数据库表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(50),nullable=False)
    name:Mapped[str] = mapped_column(String(20),nullable=False)
    password:Mapped[str] = mapped_column(String(100))
    gender:Mapped[int] = mapped_column(Integer,nullable=False)
    phone:Mapped[str] = mapped_column(String(20),nullable=False)
    job:Mapped[int] = mapped_column(Integer)
    salary:Mapped[float] = mapped_column(Float)
    deptId:Mapped[int] = mapped_column(Integer,name="dept_id")
    image:Mapped[str] = mapped_column(String(200))
    #入职时间
    entryDate:Mapped[datetime] = mapped_column(DateTime,name="entry_date")
    # 创建时间
    createTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(),name="create_time")
    # 更新时间
    updateTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),name="update_time")

