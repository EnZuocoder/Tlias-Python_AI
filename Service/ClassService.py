from datetime import  date
from sqlalchemy import select, func
from Model.ClassModel import ClassModel
from Model.EmpModel import EmpModel


async def getClazzs(name, begin, end, page, pageSize, db):
    conds = []  # 存放查询条件是否成立的bool列表
    if name and name != "":
        conds.append(ClassModel.name.like(f"%{name}%"))
    if begin is not None and end is not None:
        conds.append(ClassModel.endDate.between(begin, end))
    # 基础查询(联查员工表，用于获取班主任信息)
    baseSql = select(ClassModel, EmpModel).join(
        EmpModel, ClassModel.masterId == EmpModel.id, isouter=True)

    if conds:
        baseSql = baseSql.where(*conds)
    baseSql = baseSql.offset((page - 1) * pageSize).limit(pageSize)
    result = await db.execute(baseSql)
    rows = result.all()  # 每行是 (ClassModel,EmpModel)
    # 计数查询（不带分页,在指定条件下的总记录数）
    countSql = select(func.count()).select_from(ClassModel)
    if conds:
        countSql = countSql.where(*conds)
    total = await db.scalar(countSql)  # 返回匹配的总记录数
    #构建返回值
    clazzs = []
    for clazz, emp in rows:
        clazz.masterName = emp.name if emp else None
        clazzs.append(clazz)
    #对clazzs中的每条数据,根据当前时间和开始时间,结束时间进行比较,设置一个状态属性
    for clazz in clazzs:
        if clazz.beginDate > date.today():
            clazz.status = "未开班"
        elif clazz.endDate < date.today():
            clazz.status = "已结课"
        else:
            clazz.status = "已开班"
    return {"total": total, "rows": clazzs}


async def deleteClazz(id, db):
    clazz=await db.get(ClassModel, id)
    if clazz:
        await db.delete(clazz)
        await db.commit()
        return True
    return False


async def addClazz(newClazz, db):
    clazz = ClassModel(**newClazz.dict())
    db.add(clazz)
    await db.commit()
    return True


async def getClazzById(id, db):
    result=await db.execute(select(ClassModel).where(ClassModel.id == id))
    clazz=result.scalar_one_or_none()
    return clazz


async def updateClazz(updatedClazz, db):
    clazz = await db.get(ClassModel, updatedClazz.id)
    if clazz:
        for key, value in updatedClazz.dict().items():
            setattr(clazz, key, value)
        await db.commit()
        return True
    return False


async def getAllClazzs(db):
    result = await db.execute(select(ClassModel))
    return result.scalars().all()