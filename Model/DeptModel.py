from datetime import datetime
from sqlalchemy import  String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from Model.Base import Base
#部门模型类
class DeptModel(Base):
    __tablename__ = "dept"  # 数据库表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(50),nullable=False)
    # 创建时间
    createTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(),name="create_time")
    # 更新时间
    updateTime: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),name="update_time")

