from fastapi import APIRouter

from Pojo.Result import Result
from Utils.AI_assistant import chatWithAI, clearContext

router=APIRouter(prefix="/AIChat",tags=["AIChat"])
@router.get("")
async def chat(message: str):
    result={"AIResponse":chatWithAI(message)}
    return Result.success(result)
@router.delete("")
async def clear():
    clearContext()
    return Result.success()

