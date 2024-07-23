# SRT Summarization Service

Этот проект предоставляет API для парсинга SRT файлов и суммаризации текста с использованием FastAPI и LLM. Проект упакован в Docker.

## Установка

### Требования

- Docker

## Запуск проекта

1. **Склонируйте репозиторий**:

   ```sh
   git clone https://github.com/sumrako/summarization_srt.git
   cd summarization_srt
   ```

2. **Вставьте свой .env файлв корень проекта по примеру example.env (авторизационные данные с https://developers.sber.ru/studio)**

3. **Построить Docker образ**:
    
    ```sh
    docker build -t summarization_srt .
    ```

4. **Запустить Docker контейнер**:

    ```sh
    docker run -d -p 8000:8000 --name summarization_srt summarization_srt
    ```

Сервис будет доступен по адресу http://localhost:8000

## Тестирование
Запуск тестов внутри Docker контейнера

```sh
docker run --rm summarization_srt pytest
```