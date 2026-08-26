# RAG-генератор ответов по инструкции управления web-сервером.
# Использует Ollama + FAISS + LangChain.

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ---------- 1. Текст инструкции (источник знаний) ----------
INSTRUCTION = """
Для запуска сервера выполните команду: python web_server.py --port 8080.
Если порт занят, используйте --port 9000.
Логирование включается флагом --log-level <log level>.
Остановить сервер можно командой: kill <pid>.
Где pid - ID запущенного процесса web-сервера, log_level - уровень логирования.
"""

# Разбиваем инструкцию на осмысленные фрагменты (chunks).
# Каждый фрагмент — отдельное правило, чтобы ретривер находил именно нужное.
chunks = [
    "Для запуска сервера выполните команду: python web_server.py --port 8080.",
    "Если порт 8080 занят, используйте альтернативный порт командой: python web_server.py --port 9000.",
    "Логирование включается флагом --log-level <log level>, где log_level — уровень логирования.",
    "Остановить сервер можно командой: kill <pid>, где pid — ID запущенного процесса web-сервера.",
]

# ---------- 2. Инициализация эмбеддингов и LLM через Ollama ----------
# Модель эмбеддингов превращает текст в вектор для поиска по смыслу.
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Чат-модель, которая будет генерировать итоговый ответ.
llm = ChatOllama(model="llama3.2", temperature=0)

# ---------- 3. Создание векторного хранилища FAISS ----------
# Из списка фрагментов строим индекс, по которому потом ищем контекст.
vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

# Retriever — компонент, возвращающий наиболее релевантные фрагменты.
# k=2 означает, что будем брать 2 самых подходящих куска инструкции.
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ---------- 4. Промпт для LLM ----------
# Говорим модели: отвечай ТОЛЬКО на основе найденного контекста.
prompt = ChatPromptTemplate.from_template(
    """Ты — помощник по управлению web-сервером.
Отвечай пользователю строго на основе инструкции."

Инструкция:
{context}

Вопрос пользователя: {question}

Ответ:"""
)

# ---------- 5. Сборка RAG-цепочки ----------
# Формируем контекст: retriever возвращает список документов,
# объединяем их в одну строку через перенос.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,  # извлекаем релевантные фрагменты
        "question": RunnablePassthrough(),   # передаём вопрос как есть
    }
    | prompt                                 # подставляем в промпт
    | llm                                    # отдаём в LLM
    | StrOutputParser()                      # парсим ответ в строку
)

# ---------- 6. Интерактивный цикл ----------
def main():
    print("=" * 60)
    print("RAG-помощник по управлению web-сервером")
    print("Введите 'exit' или 'quit' для выхода.")
    print("=" * 60)

    while True:
        try:
            user_query = input("\nВаш вопрос: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение работы.")
            break

        if not user_query:
            continue
        if user_query.lower() in {"exit", "quit", "выход"}:
            print("Завершение работы.")
            break

        # Вызываем RAG-цепочку и печатаем ответ.
        answer = rag_chain.invoke(user_query)
        print("\nОтвет:", answer)

if __name__ == "__main__":
    main()