from datetime import datetime, timedelta
from typing import Dict
import jwt
# 秘钥与算法配置
_SECRET = "ThisIsA32BytePlusSecretKeyForHS25612345"
_ALGORITHM = "HS256"
_EXP_SECONDS = 60 * 60  # 1 hour
class JwtUtils:
    # 根据传入的claims生成token
    @staticmethod
    def createToken(claims: Dict) -> str:

        if claims is None:
            payload = {}
        else:
            payload = dict(claims)


        now=datetime.now()
        payload["iat"] = int(now.timestamp())
        payload["exp"] = int((now + timedelta(seconds=_EXP_SECONDS)).timestamp())

        token = jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    # 解析token
    @staticmethod
    def parseToken(token: str) -> Dict:
        try:
            payload = jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return {}
        except jwt.InvalidTokenError:
            return {}
