# Отчёт по лабораторной работе: «Glossary App на FastAPI»

## 1. Цель и задачи лабораторной работы

В ходе выполнения лабораторной работы необходимо было создать сервис на базе **FastAPI** для управления терминологическим глоссарием (словарём терминов). Основные задачи:

- Реализовать операции CRUD над терминами (создание, чтение, обновление, удаление).
- Использовать **Pydantic** для валидации входных данных и генерации схем ответов.
- Обеспечить хранение данных в **SQLite**.
- Сгенерировать **OpenAPI**-спецификацию и предоставить к ней Swagger UI / ReDoc документацию.
- (Дополнительно) Сформировать статический вариант документации на основе OpenAPI-спецификации.
- (Дополнительно) Организовать запуск приложения через Docker и выполнить деплой на сервере (VDS) с использованием HTTPS.

## 2. Структура проекта

```bash
pyweb2024-lab7
├── Dockerfile
├── README.md
├── database.db
├── main.py
├── models.py
└── requirements.txt
```

1. **main.py**  
   Содержит точку входа в приложение FastAPI и роуты (эндпоинты) для CRUD-операций.
2. **app/models.py**  
   Описание таблицы `terms` при помощи SQLModel.
3. **Dockerfile**  
   Файл, позволяющий упаковать приложение в Docker-контейнер (если используется).

## 3. Используемые технологии

- **Python 3.10+**, фреймворк **FastAPI**
- **SQLModel** для взаимодействия с SQLite
- (Опционально) **Docker** для контейнеризации

## 4. Инструкция по запуску (локально)

1. **Клонирование репозитория**:
   ```bash
   git clone <URL_репозитория>
   cd pyweb2024-lab7
   ```
2. **Установка зависимостей** (рекомендуется использовать виртуальное окружение):
   ```bash
   pip install -r requirements.txt
   pip install "fastapi[standard]"
   ```
3. **Запуск приложения**:
   ```bash
   fastapi run main.py
   ```
4. **Проверка работы**:
    - Перейдите в браузере на [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) для доступа к Swagger UI.
    - Или [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) для Redoc.

## 5. Запуск в Docker (при необходимости)

1. Убедитесь, что Docker установлен.
2. Соберите образ:
   ```bash
   docker build -t pyweb2024-lab7 .
   ```
3. Запустите контейнер:
   ```bash
   docker run -d --name pyweb2024-lab7 -p 8000:8000 pyweb2024-lab7
   ```
4. Приложение станет доступно на `http://127.0.0.1:8000`.
