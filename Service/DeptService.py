from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from Model.DeptModel import DeptModel
async def getDepts(db: AsyncSession):
    result=await db.execute(select(DeptModel))
    depts=result.scalars().all()
    return depts


async def deleteDept(Id, db):
    result=await db.execute(select(DeptModel).where(DeptModel.id==Id))
    dept=result.scalar_one_or_none()
    if dept:
        await db.delete(dept)
        await db.commit()
        return True
    return False


async def addDept(newDept, db):
    dept=DeptModel(**newDept.dict())
    db.add(dept)
    await db.commit()
    return True


async def getDeptById(id, db):
    result=await db.execute(select(DeptModel).where(DeptModel.id==id))
    dept=result.scalar_one_or_none()
    return dept
async def updateDept(updatedDept, db):
    # result=await db.execute(select(DeptModel).where(DeptModel.id==updatedDept.id))
    # dept=result.scalar_one_or_none()
    # if dept:
    #     db.merge(DeptModel(**updatedDept.dict()))
    #     await db.commit()
    #     return True
    # return False
    dept=await db.get(DeptModel,updatedDept.id)
    if dept:
        for key,value in updatedDept.dict().items():
            setattr(dept,key,value)
        await db.commit()
        return True
    return False