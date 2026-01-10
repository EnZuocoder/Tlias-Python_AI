from sqlalchemy import select, func, delete
from Model.EmpModel import EmpModel
from Model.ClassModel import ClassModel
from Model.StudentModel import StudentModel
async def getEmpGenderData(db):
    res=[]
    sql=select(EmpModel).with_only_columns(EmpModel.gender,func.count().label("value")).group_by(EmpModel.gender)
    result=await db.execute(sql)
    for row in result:
        res.append({"name": "男性员工" if row[0] == 1 else "女性员工", "value": row[1]})
    return res
async def getEmpJobData(db):
    jobList = []
    dataList = []
    sql = select(EmpModel).with_only_columns(EmpModel.job, func.count().label("value")).group_by(EmpModel.job)
    result = await db.execute(sql)
    jobDict = {1: "班主任", 2: "讲师", 3: "咨询师", 4: "学工主管", 5: "教研主管"}
    for row in result:
        jobList.append(jobDict.get(row[0], "其他"))
        dataList.append(row[1])
    return {"jobList": jobList, "dataList": dataList}


async def getStudentDegreeData(db):
    res = []
    sql = select(StudentModel).with_only_columns(StudentModel.degree, func.count().label("value")).group_by(StudentModel.degree)
    result = await db.execute(sql)
    degreeDict = {1: "初中", 2: "高中", 3: "大专", 4: "本科", 5: "硕士", 6: "博士"}
    for row in result:
        res.append({"name": degreeDict.get(row[0], "其他"), "value": row[1]})
    return res
async def getStudentCountData(db):
    res = dict()
    clazzList = []
    dataList = []
    sql=select(ClassModel.name, func.count(StudentModel.id)).join(StudentModel, ClassModel.id == StudentModel.clazzId).group_by(ClassModel.name)
    result = await db.execute(sql)
    for row in result:
        clazzList.append(row[0])
        dataList.append(row[1])
    res["clazzList"] = clazzList
    res["dataList"] = dataList
    return res