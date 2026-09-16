from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings
from app.prompts import SYSTEM_PROMPT
from app.tools.sql_tool import sql_tool
from app.tools.rag_tool import rag_tool

def create_agent():
    """Create and configure the LLM agent."""
    
    # Увеличиваем таймаут до 10 минут (600 секунд)
    llm = Ollama(
        model="qwen2.5:7b",
        base_url="http://ollama:11434",
        request_timeout=600.0,  # ← БЫЛО 120.0, СТАЛО 600.0
        temperature=0.7
    )
    
    # Устанавливаем LLM глобально (важно для RAG)
    Settings.llm = llm
    
    # Setup tools
    tools = [sql_tool]
    if rag_tool:
        tools.append(rag_tool)
    
    # Уменьшаем max_iterations, чтобы агент не зацикливался
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        max_iterations=5  # ← БЫЛО 10, СТАЛО 5 (меньше итераций = быстрее)
    )
    
    return agent

# Global agent instance
agent = create_agent()