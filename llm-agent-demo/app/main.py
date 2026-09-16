from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import agent
import traceback
import asyncio

app = FastAPI(title="LLM Agent Security Demo")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Запускаем агент в отдельном потоке с таймаутом 9 минут
        response = await asyncio.wait_for(
            asyncio.to_thread(agent.chat, request.message),
            timeout=540.0  # 9 минут (чуть меньше, чем timeout в Ollama)
        )
        return ChatResponse(response=str(response))
    except asyncio.TimeoutError:
        return ChatResponse(
            response="⚠️ ТАЙМАУТ: Агент не успел ответить за 9 минут. "
                     "Это может быть признаком DoS-атаки через сложный запрос."
        )
    except Exception as e:
        error_details = traceback.format_exc()
        return ChatResponse(
            response=f"⚠️ КРИТИЧЕСКИЙ СБОЙ АГЕНТА:\n\n"
                     f"Причина: {str(e)}\n\n"
                     f"Трассировка:\n{error_details}"
        )

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/warmup")
async def warmup():
    """Прогрев модели — загрузка в RAM."""
    try:
        response = agent.chat("Привет")
        return {"status": "Модель прогрета", "response": str(response)[:100]}
    except Exception as e:
        return {"status": "Ошибка прогрева", "error": str(e)}