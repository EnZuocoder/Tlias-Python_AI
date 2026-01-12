# python
import os
from typing import Optional

from fastapi.openapi.models import APIKey
from openai import OpenAI
_client: Optional[OpenAI] = None
_clientLocal: Optional[OpenAI] = None
_message_context = [
    {"role": "system", "content": "你是我的Tlias智能学习辅助系统的网站助理"}
]
localmodels="deepseek-r1:7b"
#初始化云端AI客户端
def _get_clientCloud() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("环境变量 DEEPSEEK_API_KEY 未设置")
        _client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    return _client
#与云端 DeepSeek AI 对话
def chatWithCloudAI(user_message: str) -> str:
    client = _get_clientCloud()
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

#初始化本地AI客户端
def _get_clientLocal() -> OpenAI:
    global _clientLocal
    if _clientLocal is None:
        # Ollama 兼容 OpenAI API，地址通常为 http://localhost:11434/v1
        _clientLocal = OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")
    return _clientLocal
#与本地 Ollama上部署的模型对话
def chatWithLocalAI(user_message: str) :
    client = _get_clientLocal()
    global _message_context
    _message_context.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model=localmodels,
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
