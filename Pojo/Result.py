#标准返回结果类
class Result:
    def __init__(self, code: int, message: str, data):
        self.code = code
        self.message = message
        self.data = data
    @staticmethod
    def success(data=None):
        return {
            "code": 1,
            "message": "success",
            "data": data
        }
    @staticmethod
    def failure(message):
        return {
            "code": 0,
            "message": message,
            "data": None
        }
"""
{
  "code": 1,
  "msg": "success",
  "data": {
    "AIResponse": "xxx"
  }
}
"""