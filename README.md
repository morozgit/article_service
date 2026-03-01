# Backend-сервис для системы отслеживания просмотров статей


## Установка 

Установите [python3](https://realpython.com/installing-python/).

## Репозиторий
Клонируйте репозиторий в удобную папку.

## Виртуальное окружение
В терминале перейдите в папку с репозиторием.

### Создание виртуального окружения
```bush 
python3 -m src/venv venv
```

### Активация виртуального окружения Linux

```bush
source src/venv/bin/activate
```


### Установка библиотек

```bush 
pip3 install -r src/requirements.txt
```
## Переменные окружения

### Создайте два файла в корне проекта
Примеры

- .env.local
  ```
    DEBUG=True
    SECRET_KEY = "supersecret"
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    REDIS_URL=redis://redis:6379/1
  ```

  - .env.docker
  ```
    DEBUG=True
    SECRET_KEY = "supersecret"
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

    REDIS_URL=redis://redis:6379/1
  ```

## Запуск


- Из корня проекта сделайте миграцию и запустите сервер Django

```bash
python3 manage.py src/migrate
python3 manage.py src/runserver
```

## Запуск в Docker
Установить [Docker](https://docs.docker.com/engine/install/ubuntu/)

Установить [Docker compose](https://docs.docker.com/compose/install/linux/)

Из корня проекта запустить
```
docker compose up --build
```