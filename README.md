# Дипломная работа для fullstack-разработчика - облачное хранилище

## Frontend
Код клиентской части приложения находится по ссыдке:
https://github.com/Sergio210-05/file_sharing.git

Сборка клиентской части находится в папке dist

## Backend
### Инструкция по развертыванию проекта на сервере

1. Терминал
Откройте терминал


2. SSH
Для доступа на сервер необходим публичный ключ ssh из файла, который находтся в файле C:\Users\[имя_пользователя]\.ssh\id_rsa.pub
Если он не создавался ранее, то его можно сгенерировать командой:
```bash
ssh-keygen
```

3. Подключение к серверу

Введите команду (после символа @ введите IP-адрес Вашего сервера):
```bash
ssh root@193.227.241.7
```
Далее подтвердите согласие и введите пароль пользователя root, который был прислан на почту при заказе сервера.

Если при заказе сервера ssh-ключ не был указан, его можно добавить в файл autorized_keys:
```bash
nano .ssh/autorized_keys
```

4. Создание нового пользователя

Введите команду:
```bash
adduser [имя_пользователя]
```

Назначение его суперпользователем:
```bash
usermod [имя_пользователя] -aG sudo
```

Переключитесь на вновь созданного пользователя:
```bash
sudo -i -u [имя_пользователя]
```

6. Установка программ и пакетов

Проверить установленные версии python и git можно командами:
```bash
python3 --version
```
```bash
git --version
```

Обновление пакетного менеджера и библиотек:
```bash
sudo apt update
```
```bash
sudo apt upgrade
```

Установка необходимых библиотек (виртуальное окружение, pip, БД postgresql, nginx):
```bash
sudo apt install python3-venv python3-pip postgresql nginx
```

Проверить запуск postgresql:
```bash
sudo systemctl status postgresql
```
Если postgresql не запустился автоматически:
```bash
sudo systemctl start postgresql
```

7. Создание базы данных (БД)

Создание нового пользователя в postreSQL:
```bash
sudo su postgres
```
```bash
psql
```
```bash
CREATE USER [имя_пользователя] WITH SUPERUSER;
```
```bash
ALTER USER [имя_пользователя] WITH PASSWORD "[пароль]";
```

Создание БД с именем пользователя:
```bash
CREATE DATABASE [имя_пользователя];
```
Выход из пользователя postgres
```bash
\q
```
```bash
exit
```

Командная строка должна начинаться с [имя_пользователя]
Подключение к postgres через нового пользователя
```bash
psql
```
Создание БД для проекта:
```bash
CREATE DATABASE diploma_storage;
```
Выход
```bash
\q
```

8. Клонирование проекта
Скопируйте клиентскую часть приложения в папку frontend корня командой:
```bash
git clone https://github.com/Sergio210-05/file_sharing.git frontend
```

Если проект разворачивается на другом сервере (не 193.227.241.7), то нужно в файле index*.js заменить IP-адрес
Введите команду 
```bash
cd frontend/file_sharing/dist/assets/
```
Проверить файлы в данном кателоге командой:
```bash
ls
```
В папке должно быть 2 файла - с расширением .css и .js
Открыть файл js:
```bash
nano [имя_файла_js]
```
Сочетанием клавиш Ctrl+W открыть поиск и найти строку со старым адресом 193.227.241.7, заменить его на нужный IP
Вернуться в корень
```bash
cd ~
```

Скопируйте серверную часть приложения в папку file_sharing_backend корня командой:
```bash
git clone https://github.com/Sergio210-05/file_sharing_backend.git file_sharing_backend
```
9. Виртуальное окружение
Перейдите в каталог file_sharing_backend:
```bash
cd file_sharing_backend
```
Создайте виртуальное окружение командой
```bash
python3 -m venv venv
```
Активируйте виртуальное окружение:
```bash
source venv/bin/activate
```
В начале строки терминала должно появиться имя окружения в скобках. 
Пример: (venv) sergio@cvXXXXXXX:~/file_sharing_backend$

10. Установка зависимостей проекта из файла requirements.txt
Выполните команду:
```bash
pip install -r requirements.txt
```
11. Создание миграций для базы данных
Выполните команду:
```bash
python manage.py migrate
```
12. Создание суперпользователя
Выполните команды:
```bash
cd file_sharing
```
```bash
python manage.py shell
```
```bash
from autentification import User
```
```bash
User.objects.create_superuser(username='admin1', full_name='admin', email='admin@mail.ru', password='Admin1@')
```

Можно указать другие учётные данные для регистрации
Выход:
Сочетание клавиш Ctrl+C

13. Настройка gunicorn
Находясь в папке проекта (папка в которой находится manage.py) выполнить команду:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
В открывшемся файле прописать:
```bash
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=[имя_пользователя]
Group=www-data
WorkingDirectory=/home/[имя_пользователя]/file_sharing_backend/file_sharing
ExecStart=/home/[имя_пользователя]/file_sharing_backend/venv/bin/gunicorn --access-logfile - \
          --workers=3 --bind unix:/home/[имя_пользователя]/file_sharing_backend/file_sharing/file_sharing/project.sock file_sharing.wsgi:application

[Install]
WantedBy=multi-user.target
```
Сохраняем файл (Ctrl+S), выходим из nano (Ctrl+X)
Запуск gunicorn:
```bash
sudo systemctl start gunicorn
```
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable gunicorn
```
```bash
sudo systemctl status gunicorn
```
В отчёте зелёным должно быть подсвечено "Active(running)"


14. Настройка nginx
Находясь в папке проекта (папка в которой находится manage.py) выполнить команду:
```bash
sudo nano /etc/nginx/sites-available/file_sharing
```

В нём прописать:
```bash
server {
  listen 80;
  server_name 193.227.241.7; (или IP Вашего сервера)

  location /static/ {
    root /home/[имя_пользователя]/file_sharing_backend/file_sharing;
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/home/[имя_пользователя]/file_sharing_backend/file_sharing/file_sharing/project.sock;
  }
}
```

Сохранить изменения (Ctrl+S), закрыть файл (Ctrl+X).

Выполнить:
```bash
sudo ln -s /etc/nginx/sites-available/file_sharing /etc/nginx/sites-enabled
```
```bash
sudo systemctl stop nginx
```
```bash
sudo systemctl start nginx
```
```bash
sudo systemctl status nginx
```

Разрешаем nginx подключение:
```bash
sudo ufw allow 'Nginx Full'
```

15. Сбор "статики"

Находясь в папке проекта (папка в которой находится manage.py) выполнить команду:
```bash
python manage.py collectstatic
```

16. Проверка работы приложения

Открыть браузер, ввести в поисковую строку IP-адрес сервера (в данном случае 95.163.221.194)

Если появляется ошибка 502 Bad Gateway, то причина может быть в отсутствии прав.

Для проверки выполнить команду в терминале:
```bash
namei -nom /home/[имя_пользователя]/file_sharing_backend/file_sharing/file_sharing/project.sock
```

Пример вывода с ошибкой в правах:

f: /home/[имя_пользователя]/file_sharing_backend/file_sharing/file_sharing/project.sock  
  drwxr-xr-x root  root 	/  
  drwxr-xr-x root  root 	home  
  drwxr-x--- [имя_пользователя] [имя_пользователя]	[имя_пользователя] <--  Здесь нехватает прав для чтения файла  
  drwxrwxr-x [имя_пользователя] [имя_пользователя]	file_sharing_backend  
  srwxrwxrwx [имя_пользователя] www-data project.sock  

Для исправления ошибки введите команду:
```bash
sudo chmod 755 /home/[имя_пользователя]
```

После исправления прав вывод namei будет отображаться следующим образом:

f: /home/[имя_пользователя]/file_sharing_backend/file_sharing/file_sharing/project.sock  
  drwxr-xr-x root  root 	/  
  drwxr-xr-x root  root 	home  
  drwxr-xr-x [имя_пользователя] [имя_пользователя]	[имя_пользователя] <- Здесь нехватает прав для чтения файла  
  drwxr-xr-x [имя_пользователя] [имя_пользователя]	file_sharing_backend  
  srwxrwxrwx [имя_пользователя] www-data project.sock  
