from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
from Pojo.Emp import Emp
from Pojo.EmpQueryParams import EmpQueryParams
from Pojo.Result import Result
from Service import EmpService
router = APIRouter(prefix="/emps", tags=["emps"])
# 获取所有员工信息(不包含工作经历,包含部门信息)
# 同时涉及分页,条件查询
@router.get("")
async def getEmps(params: EmpQueryParams = Depends(),db: AsyncSession = Depends(get_db)):
    # 从模型中解构参数，传递给服务层
    result = await EmpService.getEmps(
        name=params.name,
        gender=params.gender,
        begin=params.begin,
        end=params.end,
        page=params.page,
        pageSize=params.pageSize,
        db=db
    )
    return Result.success(result)
# 批量删除员工
#还未实现的功能:删除员工时,同时删除该员工的工作经历信息
@router.delete("")
async def deleteEmp(ids: str, db: AsyncSession = Depends(get_db)):
    idList=list(map(int,ids.split(",")))
    result = await EmpService.deleteEmp(idList, db)
    if result:
        return Result.success()
    else:
        return Result.failure("删除失败,员工不存在")
# 添加员工
@router.post("")
async def addEmp(emp: Emp, db: AsyncSession = Depends(get_db)):
    await EmpService.addEmp(emp, db)
    return Result.success()
@router.get("/{id:int}")
async def getEmpById(id: int, db: AsyncSession = Depends(get_db)):
    result = await EmpService.getEmpById(id, db)
    if result:
        return Result.success(result)
    else:
        return Result.failure("查询失败,员工不存在")
# 更新员工
@router.put("")
async def updateEmp(updatedEmp: Emp, db: AsyncSession = Depends(get_db)):
    await EmpService.updateEmp(updatedEmp, db)
    return Result.success()
# 获取所有员工信息(不包含工作经历,不包含部门信息)
@router.get("/list")
async def getAllEmps(db: AsyncSession = Depends(get_db)):
    result = await EmpService.getAllEmps(db)
    return Result.success(result)

