# Alar Studios Backend Test Task
Тестовое задание Alar Studios

## Использованный стек:
    - Python 3.10
    - FastAPI
    - PostgreSQL
    - SQLAlchemy
    - asyncio
    - React

N.B! Задание выполнялось и тестировалось в MacOS. При запуске из других ОС 
возможны проблемы с ip-адресами докер-контейнеров. 

Предпочтителен запуск через docker-compose.
Команда: 
```
docker-compose up -d
```
Такое решение комфортнее, т.к. не нужно будет отдельно настраивать БД и 2 сервера
json-server, которые применяются при решении второй части.


Тем не менее, оставлю инструкцию для запуска без docker (этапы установки библиотек не описываю):
1) Нужно будет внести новые сведения о БД в файле app.config. 
Переменные с префиксом postgres*;
2) Перед первым запуском убедиться что в PostgreSQL создана БД с названием как у
параметра postgres_database (запуск в докере делает это самостоятельно);
3) При запуске база будет заполнена стартовыми значениями. Созданный пользователь по-умолчанию
это admin:admin с правами admin;
4) Далее нужно будет запустить фронт. Для этого нужно установить на ПК node и после
вызвать команду ```npm install```. Когда библиотеки для фронта будут установлены, 
вызвать команду ```npm start``` (все эти действия совершать в папке alar_front);
5) Для работы второй части необходимо установить на ПК пакеты json-server. Позволяет
используя только json файл поднять RestFull веб-сервер. Команда - npm install -g json-server.
6) Далее запустить два сервера. Команды: 
- ```json-server --watch data1/db.json --port 3001```
- ```json-server --watch data2/db.json --port 3002```
7) Сервера не умеют работать в режиме демона, поэтому следует запускать из двух разных 
инстансов терминала. Также следует в этом случае изменить поле json_server_host в файле
app.config на "127.0.0.1";
8) Для старта бэкенда нужно вызвать команду ```python start.py```  
9) На этом этапе приложение уже должно быть работоспособно.


Если запуск проводился через docker-compose, то достаточно перейти по ссылке
http://localhost:188/.


Задачи:
1. Пользователи
    Функционал реализован полностью в соответствии с заданием.
    Логин реализован с использованием JWT (реализован только access). Пароли не шифруются.
    При первом входе будет предложено залогиниться. (Возможна проблема с компонентом логина и 
    данные потребуется ввести дважды). Срок жизни токена - 1 час. После истечения срока данные 
    с бэка получить невозможно. Потребуется разлогиниться и повторить вход.


2. Python, асинхронные запросы.
    Реализовано с использованием библиотеки asyncio и асинхронных очередей.
    Для передачи данных подготовлены 2 сервера, на одном из них хранятся данные 
    1 и 3 источников.
    Реализованы обработки ошибки по тайм-ауту и получение пустого ответа.
    К сожалению, на реализацию через псевдо-greanthreads времени не хватило.


Если возникнут вопросы со мной можно связаться в телеграм, логин @How_RU
