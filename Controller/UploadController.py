from fastapi import APIRouter, Query, UploadFile
from Pojo.Result import Result
router=APIRouter(prefix="/upload", tags=["upload"])
from Utils.aliyunoss import upload
# 上传文件到阿里云OSS
@router.post("")
async def uploadFile(file: UploadFile):
    url=await upload(file)
    print(url)
    return Result.success(url)