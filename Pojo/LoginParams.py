from pydantic import BaseModel

#put请求,记录登录参数
class LoginParams(BaseModel):
    username: str
    password: str