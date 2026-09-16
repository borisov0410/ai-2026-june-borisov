from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import agent
from app.security import check_input_guard, apply_output_guard
import asyncio

app = FastAPI(title="Secure LLM Agent Demo")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Input Guard
    is_safe, error_msg = check_input_guard(request.message)
    if not is_safe:
        return ChatResponse(response=error_msg)

    try:
        # 2. Выполнение агента
        response = await asyncio.wait_for(
            asyncio.to_thread(agent.chat, request.message),
            timeout=540.0
        )
        
        # 3. Output Guard
        raw_response = str(response)
        sanitized_response = apply_output_guard(raw_response)
        
        return ChatResponse(response=sanitized_response)
        
    except asyncio.TimeoutError:
        return ChatResponse(response="⛔ Access Denied: Превышено время ожидания (возможная DoS-атака).")
    except Exception as e:
        return ChatResponse(response="⛔ Access Denied: Внутренняя ошибка обработана безопасно.")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/warmup")
async def warmup():
    try:
        response = agent.chat("Привет")
        return {"status": "Модель прогрета", "response": str(response)[:50]}
    except Exception as e:
        return {"status": "Ошибка", "error": str(e)}