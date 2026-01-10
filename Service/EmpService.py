from sqlalchemy import select, func, delete
from Model.DeptModel import DeptModel
from Model.EmpExprModel import EmpExprModel
from Model.EmpModel import EmpModel
from Utils.aliyunoss import deleteFromOss


# from Utils.aliyunoss import deleteObject


#条件,分页查询,结合部门信息联查
async def getEmps(name, gender, begin, end, page, pageSize, db):
    conds = [] # 存放查询条件是否成立的bool列表
    if name and name != "":
        conds.append(EmpModel.name.like(f"%{name}%"))
    if gender is not None:
        conds.append(EmpModel.gender == gender)
    if begin is not None and end is not None:
        conds.append(EmpModel.entryDate.between(begin, end))
    # 基础查询（用于取分页数据）
    base_stmt = select(EmpModel, DeptModel).join(
        DeptModel, EmpModel.deptId == DeptModel.id, isouter=True
    )
    if conds:
        base_stmt = base_stmt.where(*conds)
    base_stmt = base_stmt.offset((page - 1) * pageSize).limit(pageSize)
    result = await db.execute(base_stmt)
    rows = result.all()  # 每行是 (EmpModel, DeptModel)
    # 计数查询（不带分页,在指定条件下的总记录数）
    count_stmt = select(func.count()).select_from(EmpModel).join(
        DeptModel, EmpModel.deptId == DeptModel.id, isouter=True
    )
    if conds:
        count_stmt = count_stmt.where(*conds)
    total = await db.scalar(count_stmt)  # 返回匹配的总记录数

    emps = []
    for emp, dept in rows:
        emp.deptName = dept.name if dept else None
        emps.append(emp)
    return {"total": total, "rows": emps}

# 批量删除员工
async def deleteEmp(Ids, db):
    #删除员工时,还要删除阿里云上的头像文件
    for id in Ids:
        emp = await db.get(EmpModel, id)
        print(emp.image)
        if emp and emp.image:
            deleteFromOss(emp.image)
    sql1=delete(EmpModel).where(EmpModel.id.in_(Ids))
    await db.execute(sql1)
    sql2=delete(EmpExprModel).where(EmpExprModel.empId.in_(Ids))
    await db.execute(sql2)
    await db.commit()
    return True
# 添加员工
async def addEmp(emp, db):
    exprlist = emp.exprList
    emp_data=emp.dict(exclude={"exprList"})
    empModel = EmpModel(**emp_data)
    db.add(empModel)
    await db.flush()  # 刷新以获取自增主键ID
    for e in exprlist:
        empExprModel = EmpExprModel(**e, empId=empModel.id)
        db.add(empExprModel)

    await db.commit()
    return True


async def getEmpById(id, db):
    result = await db.execute(select(EmpModel).where(EmpModel.id == id))
    emp = result.scalar_one_or_none()
    if emp:
        result_expr = await db.execute(select(EmpExprModel).where(EmpExprModel.empId == id))
        exprs = result_expr.scalars().all()
        emp.exprList = exprs
    return emp
async def updateEmp(updatedEmp, db):
    # 获取已有员工
    emp = await db.get(EmpModel, updatedEmp.id)
    # 提取经历列表（兼容 None）
    exprlist = getattr(updatedEmp, "exprList", [])
    # 更新员工主体字段，排除 id 和 exprList（避免修改主键）
    emp_data = updatedEmp.dict(exclude={"exprList", "id"})
    for key, value in emp_data.items():
        setattr(emp, key, value)

    # 删除原有的经历记录
    await db.execute(delete(EmpExprModel).where(EmpExprModel.empId == updatedEmp.id))

    # 重新添加传入的经历记录（忽略传入的 id 字段）
    for e in exprlist:
        e.pop("id", None)
        e["empId"] = updatedEmp.id
        empExprModel = EmpExprModel(**e)
        db.add(empExprModel)
    await db.commit()
    return True

async def getAllEmps(db):
    result = await db.execute(select(EmpModel))
    return result.scalars().all()