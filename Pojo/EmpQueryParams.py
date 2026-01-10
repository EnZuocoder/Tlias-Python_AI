from typing import Optional
from fastapi import Query
from datetime import date, datetime
#员工查询参数模型类
class EmpQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None),
        gender: Optional[str] = Query(None),#默认为字符串,实际传过来的是数字
        begin: Optional[str] = Query(None),#默认为字符串,实际传过来的是日期形式
        end: Optional[str] = Query(None),#默认为字符串,实际传过来的是日期形式
        page: int = Query(1),
        pageSize: int = Query(10),

    ):
        self.name = name.strip() if isinstance(name, str) and name.strip() else None
        #这里前端保证gender只能是""、0、1,begin 和end也只能是""或合法日期字符串
        if gender and gender !="":
            self.gender = int(gender)
        else:
            self.gender = None
        if begin and begin !="":
            self.begin = date.fromisoformat(begin)
        else:
            self.begin = None
        if end and end !="":
            self.end = date.fromisoformat(end)
        else:
            self.end = None
        self.page = page
        self.pageSize = pageSize
