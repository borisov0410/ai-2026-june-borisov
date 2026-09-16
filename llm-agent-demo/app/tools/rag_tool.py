import os
import ssl

# Обход проблемы с SSL-сертификатами при скачивании NLTK в Docker (опционально, но полезно)
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

DOCS_PATH = "/app/data/docs"

def setup_rag():
    """Initialize RAG system with internal documents."""
    
    # 1. Явно создаем экземпляр Ollama LLM
    llm = Ollama(
        model="qwen2.5:7b",
        base_url="http://ollama:11434",
        request_timeout=120.0
    )
    
    # 2. Создаем модель эмбеддингов
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # 3. Устанавливаем их как глоальные настройки по умолчанию для LlamaIndex
    # Это предотвращает попытку использовать OpenAI
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    if os.path.exists(DOCS_PATH) and os.listdir(DOCS_PATH):
        documents = SimpleDirectoryReader(DOCS_PATH).load_data()
        
        # Создаем индекс (он автоматически возьмет embed_model из Settings)
        index = VectorStoreIndex.from_documents(documents)
        
        # 4. Явно передаем llm в query_engine
        query_engine = index.as_query_engine(llm=llm)
        
        return QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name="read_internal_docs",
            description="Search and read internal company documentation and knowledge base"
        )
    
    return None

rag_tool = setup_rag()