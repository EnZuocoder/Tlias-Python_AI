from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
from Pojo.Result import Result
from Service import ReportService

router = APIRouter(prefix="/report", tags=["report"])
#员工性别数据报表统计
@router.get("/empGenderData")
async def getEmpGenderData(db: AsyncSession = Depends(get_db)):
    result = await ReportService.getEmpGenderData(db)
    return Result.success(result)
#员工职位人数统计
@router.get("/empJobData")
async def getEmpJobData(db: AsyncSession = Depends(get_db)):
    result = await ReportService.getEmpJobData(db)
    return Result.success(result)
#学生学历信息统计
@router.get("/studentDegreeData")
async def getStudentDegreeData(db: AsyncSession = Depends(get_db)):
    result = await ReportService.getStudentDegreeData(db)
    return Result.success(result)

#各个班级学生人数统计
@router.get("/studentCountData")
async def getStudentCountData(db: AsyncSession = Depends(get_db)):
    result = await ReportService.getStudentCountData(db)
    return Result.success(result)
