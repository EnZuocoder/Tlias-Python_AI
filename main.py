from fastapi import FastAPI
from Controller import DeptController, EmpController, UploadController, ClassController, StudentController, \
    ReportController, LoginController, AIChatController
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from Utils.JwtUtils import JwtUtils
app = FastAPI()
#解决跨域问题
app.add_middleware(
    CORSMiddleware,
    #只允许本机的5173端口
    allow_origins=["http://localhost:5173"],  # 允许的来源,只允许本机的5173端口
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)
#挂载路由
app.include_router(DeptController.router)
app.include_router(EmpController.router)
app.include_router(UploadController.router)
app.include_router(ClassController.router)
app.include_router(StudentController.router)
app.include_router(ReportController.router)
app.include_router(LoginController.router)
app.include_router(AIChatController.router)


# 中间件,收到的所有请求除了登录请求都要验证token
@app.middleware("http")
async def checkToken(request, callNext):
    #排除登录请求
    if request.url.path.startswith("/login") or request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        response = await callNext(request)
        return response
    #验证token
    token = request.headers.get("token")
    if not token or token=="":
        return JSONResponse(content={"code":401,"message":"未提供token,请先登录"}, status_code=401)
    claims= JwtUtils.parseToken(token)
    if not claims:
        return JSONResponse(content={"code":401,"message":"token无效,请重新登录"}, status_code=401)
    #token有效,继续处理请求
    response = await callNext(request)
    return response

