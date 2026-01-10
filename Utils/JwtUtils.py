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
        """Create a JWT token from claims dict.

        - Always sets `iat` (issued at) and `exp` (expiration) to now / now+1h.
        - Uses HS256 and the module secret.
        - Returns token as a string.
        """
        if claims is None:
            payload = {}
        else:
            # make a shallow copy to avoid mutating caller's dict
            payload = dict(claims)


        now=datetime.now()
        payload["iat"] = int(now.timestamp())
        payload["exp"] = int((now + timedelta(seconds=_EXP_SECONDS)).timestamp())

        token = jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)
        # PyJWT may return bytes in some versions; normalize to str
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
