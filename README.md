Habr-team-3
===========


*This project is a child of the team development by methodology Agile: SCRUM from GeekBrains university.*

*The project is being done by team #3.*


## Базовая документация к проекту


Основные системные требования:
* Ubuntu 20.04 LTS
* Python 3.7+
* PostgreSQL 13.1
* Django 3.1.5
* Зависимости (Python) из needs.txt


### Обновляем системные зависимости


```
~$ sudo apt update
~$ sudo apt upgrade
```


### Ставим PostgreSQL, создаём пользователя и БД


Для начала установим PostgreSQL, если он еще не установлен, 
и сразу же запустим интерпретатор команд сервера
```
~$ sudo apt-get install postgresql postgresql-contrib
~$ sudo -u postgres psql
```
и выполним следующие команды для создания базы данных и пользователя, настройки привилегий
```postgresql
CREATE DATABASE database_name;
CREATE USER username with NOSUPERUSER PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;
```
и параметры подключения: кодировку, уровень изоляции транзакций, временная зона
```postgresql
ALTER ROLE username SET CLIENT_ENCODING TO 'UTF8';
ALTER ROLE username SET default_transaction_isolation TO 'READ COMMITTED';
ALTER ROLE username SET TIME ZONE 'Asia/Yekaterinburg';
```
После установки проверяем статус СУБД, командой: service postgresql status


### Ставим NGINX


Для начала установим NGINX, если он еще не установлен
```
~$ sudo apt install nginx
```
Далее настроим параметры веб-приложения, создадим файл
```
~$ sudo nano /etc/nginx/sites-available/AgileHabr
```
и пропишем следующие настройки, можно указать IP-address или доменное имя,
а так же настроим раздачу статическим и медиа файлов
```
server {
    listen 80;
    server_name <YOUR IP OR DOMAIN NAME>;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/username/AgileHabr;
    }

    location /media/ {
        root /home/username/AgileHabr;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/username/AgileHabr/AgileHabr.sock;
    }
}
```
Создаем ссылку в папке разрешенных сайтов «/etc/nginx/sites-enabled»:
```
~$ sudo ln -s /etc/nginx/sites-available/your-web-site /etc/nginx/sites-enabled
```
Проверяем настройки «nginx»:
```
~$ sudo nginx -t
```
Перезапускаем службу «nginx» и добавляем разрешения в сетевой экран:
```
~$ sudo systemctl restart nginx
~$ sudo ufw allow 'Nginx Full'
```
В случае ошибок проверяем логи сервера nginx:
```
~$ sudo tail -F /var/log/nginx/error.log
```
Миграции выполняем как обычно, переходим в коревой каталог нашего проекта и выполняем команду
```
~$ python manage.py migrate
```


### Установка зависимостей


Переходим в коревую папку нашего проекта, там где находится файл needs.txt и выполняем команду
```
~$ pip3 install -r needs.txt
```


### Выполнение миграций и сбор статических файлов проекта


Выполняем миграции из корневого каталога нашего проекта
```
~$ python3 manage.py migrate
```
Собираем статику
```
~$ python3 manage.py collectstatic
```


### Суперпользователь


Создаём суперпользователя, администратора проекта
```
~$ python3 manage.py createsuperuser
```
Говорим, к примеру (логин/пароль): admin:admin


### Установка и настройка gunicorn


Начнем с установки модуля «gunicorn»
```
~$ pip3 install gunicorn
```
Проверяем, что он работает - выполняем команду в папке проекта
```
~$ gunicorn AgileHabr.wsgi
```
Настроим параметры службы «gunicorn» для нашего проекта. Создаём файл
```
~$ sudo nano /etc/systemd/system/gunicorn.service
```
и добавляем в него следующее
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/home/username/AgileHabr
ExecStart=/usr/bin/gunicorn3 --access-logfile - --workers 3 --bind unix:/home/username/AgileHabr/AgileHabr.sock AgileHabr.wsgi

[Install]
WantedBy=multi-user.target
```
Разрешаем и запускаем службу «gunicorn», проверяем ее статус:
```
~$ sudo systemctl enable gunicorn
~$ sudo systemctl start gunicorn
~$ sudo systemctl status gunicorn
```
