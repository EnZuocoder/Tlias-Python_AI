from pydantic import Field, BaseModel
class Clazz(BaseModel):
    id: int =Field(default=None)
    name: str
    room: str
    beginDate: str
    endDate: str
    subject: int
    masterId: int
