# Проект Продуктовый помощник
![workflow status](https://github.com/maximuz2004/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Описание:
Сервис позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии:
Python 3.9.10, Django 3.2, DRF, Djoser, PostgreSQL, Docker

### Как запустить проект:
1.  Клонируйте репозиторий:
```
git@github.com:Maximuz2004/foodgram-project-react.git
```
2.  Перейдите в директорию проекта. Создайте и активируйте виртуальное окружение. Установите все зависимости:
```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt

```
3. Запустите тесты. Проверьте, что они все прошли. 
```
pytest
```
Перейдите в директорию с файлом manage.py, создайте, примените миграции и создайте суперпользователя
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Запустите сервер разработчика:
```
python manage.py runserver
```

4. Настройка удаленного сервера:

    1. Войдите на свой удаленный сервер. 
    2. Остановите службу nginx:
   ```
    sudo systemctl stop nginx
   ```
   3. Установите docker:
   ```
   sudo apt install docker.io
   ```
   4. Установите doker-compose согласно официальной [документации](https://docs.docker.com/compose/install/)

5. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

    В файле ```nginx/default.conf ``` укажите ip-адрес вашего сервера

6. Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных и всего остального:
```
ALLOWED_HOSTS - список допустимых хостов, которые могут обращаться к приложению
DB_ENGINE=django.db.backends.postgresql
DB_NAME=*имя базы данных*
POSTGRES_USER=*логин для подключения к базе данных*
POSTGRES_PASSWORD=*пароль для подключения к БД*
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=*секретный ключ Джанго*
HOST - ip-адрес вашего сервера
USER - пользователь удаленного сервера
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
DOCKER_USERNAME - ваш ник на https://hub.docker.com/
DOCKER_PASSWORD - ваш пароль на DockerHub
TELEGRAM_TO - Ваше id в Телеграмме
TELEGRAM_TOKEN - токен вашего бота в Телеграмме
```
7. Запустите проект на сервере:
```
sudo docker-compose up -d
```

Далее Выполните миграции, соберите статику, подгрузите неоходимую информацию в БД и создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py load_data
```

Проект доступен по адресу: http://130.193.34.139/recipes

## Разработчик
[Максим Титов](https://github.com/Maximuz2004)
