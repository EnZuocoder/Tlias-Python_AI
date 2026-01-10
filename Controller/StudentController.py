from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Config.DataBaseConfig import get_db
from Pojo.Result import Result
from Pojo.Student import Student
from Pojo.StudentQueryParams import StudentQueryParams
from Service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


# 条件分页查询
@router.get("")
async def getStudents(params: StudentQueryParams = Depends(), db: AsyncSession = Depends(get_db)):
    # 从模型中解构参数，传递给服务层
    result = await StudentService.getStudents(
        name=params.name,
        degree=params.degree,
        clazzId=params.clazzId,
        page=params.page,
        pageSize=params.pageSize,
        db=db
    )
    return Result.success(result)


# 删除学生
@router.delete("/{ids}")
async def deleteStudent(ids: str, db: AsyncSession = Depends(get_db)):
    idList = list(map(int, ids.split(",")))
    result = await StudentService.deleteStudent(idList, db)
    if result:
        return Result.success()
    else:
        return Result.failure("删除失败,学生不存在")


# 添加学生
@router.post("")
async def addStudent(newStudent: Student, db: AsyncSession = Depends(get_db)):
    await StudentService.addStudent(newStudent, db)
    return Result.success()


# 根据id查询
@router.get("/{id}")
async def getStudentById(id: int, db: AsyncSession = Depends(get_db)):
    result = await StudentService.getStudentsById(id, db)
    if result:
        return Result.success(result)
    else:
        return Result.failure("学生不存在")


# 编辑学生
@router.put("")
async def updateStudent(updatedStudent: Student, db: AsyncSession = Depends(get_db)):
    await StudentService.updateStudent(updatedStudent, db)
    return Result.success()

# 违纪处理
@router.put("/violation/{id}/{score}")
async def handleViolation(id: int, score: int, db: AsyncSession = Depends(get_db)):
    result = await StudentService.handleViolation(id, score, db)
    return Result.success(result)