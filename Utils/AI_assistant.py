# python
import os
from typing import Optional
from openai import OpenAI
_client: Optional[OpenAI] = None
_message_context = [
    {"role": "system", "content": "你是我的Tlias智能学习辅助系统的网站助理"}
]
def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("环境变量 DEEPSEEK_API_KEY 未设置")
        _client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    return _client

def chatWithAI(user_message: str) -> str:
    client = _get_client()
    global _message_context
    _message_context.append({"role": "user", "content": user_message})
    response =client.chat.completions.create(
        model="deepseek-chat",
        messages=_message_context,
        stream=False
    )
    ai_message = response.choices[0].message.content
    _message_context.append({"role": "assistant", "content": ai_message})
    return ai_message
#清空当前对话上下文
def clearContext():
    global _message_context
    _message_context = [
        {"role": "system", "content": "你是我的Tlias智能学习辅助系统的网站助理"}
    ]
    return True
