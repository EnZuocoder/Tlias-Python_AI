import os
import re
import uuid
from typing import BinaryIO, Union
import alibabacloud_oss_v2 as oss
from fastapi import UploadFile
from datetime import date
import urllib.parse
import logging

from sqlalchemy.orm import defer

# 配置信息
BUCKET = "java-wcx"
REGION = "cn-beijing"
ENDPOINT = "https://oss-cn-beijing.aliyuncs.com"
logger = logging.getLogger(__name__)


def _get_extension(filename: str) -> str:
    """从 filename 中提取扩展名（包含点），若无则返回空字符串"""
    if not filename:
        return ""
    return os.path.splitext(filename)[1] or ""


async def upload(file: Union[UploadFile, BinaryIO, bytes, bytearray, str]) -> str:
    """
    异步上传文件到阿里云 OSS 并返回文件 URL。
    参数:
      - file: FastAPI `UploadFile`，或 file-like（带 read/seek），或 bytes，或本地路径字符串
    返回值: 公网可访问的 URL 字符串

    上传路径会以 年份/月份 前缀保存，例如: 2026/01/<uuid>.ext

    注意: 使用环境变量方式的凭证（`OSS_ACCESS_KEY_ID` / `OSS_ACCESS_KEY_SECRET`），请确保在运行时已正确设置。
    """
    name = file.filename
    data = await file.read()
    # 生成保存到 OSS 的 key：按 年/月 前缀 + uuid 保留扩展名
    ext = _get_extension(name) if name else ""
    prefix = date.today().strftime("%Y/%m")
    key = f"{prefix}/{uuid.uuid4().hex}{ext}"
    # 使用环境变量凭证
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    client = oss.Client(cfg)
    try:
        req = oss.PutObjectRequest(
            bucket=BUCKET,
            key=key,
            body=data,
        )
        client.put_object(req)
    except Exception as e:
        raise RuntimeError(f"upload to OSS failed: {e}")
    host = ENDPOINT.replace("https://", "").replace("http://", "").rstrip("/")
    url = f"https://{BUCKET}.{host}/{key}"
    return url


def deleteFromOss(file_url: str) -> bool:

    # 从 URL 中提取 key(去除endPoint,bucket部分)
    # 使用环境变量凭证
    prefix=f"https://{BUCKET}.{ENDPOINT.replace("https://","")}/"
    key=file_url.replace(prefix,"")
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    client = oss.Client(cfg)
    try:
        req = oss.DeleteObjectRequest(
            bucket=BUCKET,
            key=key,
        )
        client.delete_object(req)
        return True
    except Exception as e:
        raise RuntimeError(f"delete from OSS failed: {e}")