from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
from Pojo.ClassQueryParams import ClassQueryParams
from Pojo.Clazz import Clazz
from Pojo.Result import Result
from Service import ClassService
router=APIRouter(prefix="/clazzs",tags=["clazzs"])
#班级列表分页查询
@router.get("")
async def getClazzs(params: ClassQueryParams = Depends(), db: AsyncSession = Depends(get_db)):
    result=await ClassService.getClazzs(
        name=params.name,
        begin=params.begin,
        end=params.end,
        page=params.page,
        pageSize=params.pageSize,
        db=db
    )
    return Result.success(result)
#删除班级
@router.delete("/{id:int}")
async def deleteClazz(id:int, db: AsyncSession = Depends(get_db)):
    result=await ClassService.deleteClazz(id, db)
    return Result.success(result)
#添加班级
@router.post("")
async def addClazz(newClazz:Clazz, db: AsyncSession = Depends(get_db)):
    result=await ClassService.addClazz(newClazz, db)
    return Result.success(result)
# 根据id查询班级
@router.get("/{id:int}")
async def getClazzById(id:int, db: AsyncSession = Depends(get_db)):
    result=await ClassService.getClazzById(id, db)
    if result:
        return Result.success(result)
    else:
        return Result.failure("查询失败,班级不存在")
# 更新班级
@router.put("")
async def updateClazz(updatedClazz:Clazz, db: AsyncSession = Depends(get_db)):
    result=await ClassService.updateClazz(updatedClazz, db)
    if result:
        return Result.success()
    else:
        return Result.failure("更新失败,班级不存在")
#查询所有班级(不分页)
@router.get("/list")
async def getAllClazzs(db: AsyncSession = Depends(get_db)):
    result=await ClassService.getAllClazzs(db)
    return Result.success(result)