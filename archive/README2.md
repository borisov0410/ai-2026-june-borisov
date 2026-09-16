Для работы скрипта должно быть установлено:

- ПО Ollama

Скачана модель llama3.2:

- ollama pull llama3.2

Обязательно! отдельно скачать модель для embeddings (пример):

- ollama pull nomic-embed-text

Установлена зависимость:

- pip install langchain langchain-ollama langchain-community faiss-cpu

Запуск скрипта:

- python homework4.py