from fastapi import APIRouter
from Pojo.Result import Result
from Utils.AI_assistant import chatWithCloudAI, clearContext, chatWithLocalAI
router=APIRouter(prefix="/AIChat",tags=["AIChat"])
@router.get("")
async def chat(message: str):
    result={"AIResponse": chatWithLocalAI(message)}
    return Result.success(result)
@router.delete("")
async def clear():
    clearContext()
    return Result.success()

