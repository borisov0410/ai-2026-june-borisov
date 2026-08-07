#!/bin/bash

# Название контейнера
CONTAINER_NAME="ollama-server"

# Остановить и удалить старый контейнер, если он существует
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Останавливаем и удаляем старый контейнер..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Запуск Ollama в Docker
echo "Запускаем Ollama в Docker..."
docker run -d \
    --name $CONTAINER_NAME \
    -p 11434:11434 \
    -v ollama_data:/root/.ollama \
    
    ollama/ollama:latest

# Ждём, пока сервер запустится
echo "Ожидаем запуска сервера..."
sleep 10

# Проверяем, что сервер доступен
echo "Проверяем доступность сервера..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Сервер Ollama успешно запущен!"
        break
    fi
    sleep 2
done

# Загружаем модель llama3
echo "Загружаем модель llama3..."
docker exec -it $CONTAINER_NAME ollama pull llama3

echo ""
echo "=== Ollama успешно запущена ==="
echo "Модель llama3 готова к использованию"
echo "Сервер доступен по адресу: http://localhost:11434"
echo ""
echo "Для взаимодействия с моделью используйте:"
echo "curl http://localhost:11434/api/generate -d '{\"model\": \"llama3\", \"prompt\": \"Hello!\"}'"