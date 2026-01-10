from pydantic import BaseModel, Field


class Emp(BaseModel):
    id:int=Field(default=None)
    name:str
    username:str
    password:str=Field(default="123456")
    gender:int
    phone:str
    job:int
    salary:float
    deptId:int
    image:str
    entryDate:str
    exprList:list