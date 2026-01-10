from pydantic import BaseModel, Field
class Student(BaseModel):
    id: int =Field(default=None)
    name:str
    no:str
    gender:int
    phone:str
    idCard:str
    isCollege:int
    address:str
    degree:int
    graduationDate:str
    clazzId:int
