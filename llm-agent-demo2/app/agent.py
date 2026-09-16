from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings
from app.prompts import SYSTEM_PROMPT
from app.tools.sql_tool import sql_tool
from app.tools.rag_tool import rag_tool

def create_agent():
    llm = Ollama(
        model="qwen2.5:7b",
        base_url="http://ollama-secure:11434",
        request_timeout=600.0,
        temperature=0.1 # Низкая температура для более детерминированного и безопасного поведения
    )
    
    Settings.llm = llm
    
    tools = [sql_tool]
    if rag_tool:
        tools.append(rag_tool)
    
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        max_iterations=5 # Защита от DoS через зацикливание
    )
    
    return agent

agent = create_agent()