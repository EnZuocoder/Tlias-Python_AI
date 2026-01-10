from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from Model.Base import Base
# 员工工作经历模型类
class EmpExprModel(Base):
    __tablename__ = "emp_expr"  # 数据库表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empId:Mapped[int] = mapped_column(Integer,name="emp_id",nullable=False)
    company:Mapped[str] = mapped_column(String(100),nullable=False)
    job:Mapped[str] = mapped_column(String(100),nullable=False)
    begin:Mapped[datetime] = mapped_column(DateTime,nullable=False)
    end:Mapped[datetime] = mapped_column(DateTime)
