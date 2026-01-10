from typing import Optional
from fastapi import Query
#学生查询参数模型类class StudentQueryParams:
class StudentQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None),
        degree: Optional[str] = Query(None),#默认为字符串,实际传过来的是数字
        clazzId: Optional[str] = Query(None),#默认为字符串,实际传过来的是数字
        page: int = Query(1),
        pageSize: int = Query(10),

    ):
        self.name = name.strip() if isinstance(name, str) and name.strip() else None
        #这里前端保证gender只能是""、0、1,begin 和end也只能是""或合法日期字符串
        if degree and degree !="":
            self.degree = int(degree)
        else:
            self.degree = None
        if clazzId and clazzId !="":
            self.clazzId = int(clazzId)
        else:
            self.clazzId = None
        self.page = page
        self.pageSize = pageSize
