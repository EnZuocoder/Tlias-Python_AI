from sqlalchemy import select
from Model.EmpModel import EmpModel
from Pojo.LoginInfo import LoginInfo
from Pojo.LoginParams import LoginParams
from Utils.JwtUtils import JwtUtils


async def login(params: LoginParams, db):
    info=LoginInfo()
    sql=(select(EmpModel).
         where(EmpModel.username==params.username,
                            EmpModel.password==params.password))
    result=await db.execute(sql)
    emp=result.scalar_one_or_none()
    m=dict()
    if emp:
        m["id"]=emp.id
        m["username"]=emp.username
        info.id=emp.id
        info.username=emp.username
        info.name=emp.name
        #根据用户的id和用户名生成token
        info.token=JwtUtils.createToken(m)
    return info