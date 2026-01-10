from sqlalchemy import select, func, delete

from Model.ClassModel import ClassModel
from Model.StudentModel import StudentModel


async def getStudents(name, degree, clazzId, page, pageSize, db):
    conds = []  # 存放查询条件是否成立的bool列表
    if name and name != "":
        conds.append(StudentModel.name.like(f"%{name}%"))
    if degree is not None:
        conds.append(StudentModel.degree == degree)
    if clazzId is not None:
        conds.append(StudentModel.clazzId == clazzId)
    # 基础查询（用于取分页数据）
    baseSql = select(StudentModel, ClassModel).join(
        ClassModel, StudentModel.clazzId == ClassModel.id, isouter=True
    )
    if conds:
        baseSql = baseSql.where(*conds)
    baseSql = baseSql.offset((page - 1) * pageSize).limit(pageSize)
    result = await db.execute(baseSql)
    rows = result.all()  # 每行是 (StudentModel, ClazzModel)
    # 计数查询（不带分页,在指定条件下的总记录数）
    countSql = select(func.count()).select_from(StudentModel)
    if conds:
        countSql = countSql.where(*conds)
    total = await db.scalar(countSql)  # 返回匹配的总记录数
    students = []
    for student, clazz in rows:
        student.clazzName = clazz.name if clazz else None
        students.append(student)
    return {"total": total, "rows": students}


async def deleteStudent(idList, db):
    sql = delete(StudentModel).where(StudentModel.id.in_(idList))
    result = await db.execute(sql)
    await db.commit()
    return result.rowcount > 0


async def addStudent(newStudent, db):
    db.add(StudentModel(**newStudent.dict()))
    await db.commit()
    return True


async def getStudentsById(id, db):
    result = await db.execute(select(StudentModel).where(StudentModel.id == id))
    return result.scalar_one_or_none()


async def updateStudent(updatedStudent, db):
    sql = (
        select(StudentModel)
        .where(StudentModel.id == updatedStudent.id)
        .with_for_update()
    )
    result = await db.execute(sql)
    student = result.scalar_one_or_none()
    if student:
        for key, value in updatedStudent.dict().items():
            setattr(student, key, value)
        await db.commit()
    return True


async def handleViolation(id, score, db):
    sql = (
        select(StudentModel)
        .where(StudentModel.id == id)
        .with_for_update()
    )
    result = await db.execute(sql)
    student = result.scalar_one_or_none()
    if student:
        student.violationCount += 1
        student.violationScore += score
        await db.commit()
    return True
