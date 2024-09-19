## Warehouse API

### Описание

Warehouse API — это RESTful API для управления складом и заказами. API позволяет создавать, читать, обновлять и удалять продукты, а также создавать и обновлять заказы. Проект разработан с использованием FastAPI и SQLAlchemy, а также поддерживает запуск в Docker с базой данных PostgreSQL.

### Технологии

- **FastAPI**: Современный, быстрый (высокопроизводительный) веб-фреймворк для создания API с Python 3.7+.
- **SQLAlchemy**: ORM для работы с базами данных.
- **PostgreSQL**: Реляционная база данных.
- **Docker**: Платформа для разработки, доставки и запуска приложений в контейнерах.
- **Docker Compose**: Инструмент для определения и запуска многоконтейнерных Docker-приложений.

### Структура проекта

```
WarehouseAPI/
│
├── database.py
├── main.py
├── models.py
├── schemas.py
├── tests/
│    └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Установка и запуск

#### 1. Установка зависимостей

Убедитесь, что у вас установлены Python 3.12, Docker и Docker Compose.

#### 2. Клонирование репозитория

```bash
git clone https://github.com/aleksey-kerkin/WarehouseAPI.git
cd WarehouseAPI
```

#### 3. Запуск с использованием Docker Compose

Для запуска проекта с использованием Docker Compose выполните следующие команды:

```bash
docker-compose up --build
```

После запуска API будет доступен по адресу `http://127.0.0.1:8000`.

#### 4. Запуск с использованием Python

Для запуска проекта с использованием Python выполните следующие команды:

1. Создайте виртуальное окружение:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

После запуска API будет доступен по адресу `http://127.0.0.1:8000`.

### Тестирование

Для запуска тестов выполните следующую команду:

```bash
pytest tests/
```

### Документация

Доступ к документации FastAPI можно получить по следующим адресам:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
