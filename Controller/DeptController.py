#部门管理请求处理路由
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
from Pojo.Dept import Dept
from Pojo.Result import Result
from Service import DeptService
router=APIRouter(prefix="/depts",tags=["depts"])
#获取所有部门信息
@router.get("")
async def getDepts(db:AsyncSession=Depends(get_db)):
    result=await DeptService.getDepts(db)
    return Result.success(result)
#删除指定部门
@router.delete("")
async def deleteDept(id:int,db:AsyncSession=Depends(get_db)):
    result=await DeptService.deleteDept(id,db)
    if result:
        return Result.success()
    else:
        return Result.failure("删除失败,部门不存在")
#添加部门
@router.post("")
async def addDept(newDept:Dept,db:AsyncSession=Depends(get_db)):
    result=await DeptService.addDept(newDept,db)
    if result:
        return Result.success()
    else:
        return Result.failure("添加失败,请稍后再试")
#根据id查询部门
@router.get("/{id}")
async def getDeptById(id:int,db:AsyncSession=Depends(get_db)):
    result=await DeptService.getDeptById(id,db)
    if result:
        return Result.success(result)
    else:
        return Result.failure("查询失败,部门不存在")
#更新部门
@router.put("")
async def updateDept(updatedDept:Dept,db:AsyncSession=Depends(get_db)):
    result=await DeptService.updateDept(updatedDept,db)
    if result:
        return Result.success()
    else:
        return Result.failure("更新失败,部门不存在")

