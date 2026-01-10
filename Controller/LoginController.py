from fastapi import APIRouter, Depends

from Pojo.LoginParams import LoginParams
from Pojo.Result import Result
from Service import LoginService
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
router = APIRouter(prefix="/login", tags=["login"])
@router.post("")
async def login(params: LoginParams, db: AsyncSession = Depends(get_db)):
    info = await LoginService.login(params, db)
    if info:
        return Result.success(info)
    else:
        return Result.failure("登录失败,用户名或密码错误")
