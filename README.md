Как запустить сервер у себя
===========================

Мы используем Python 3.3 и Django 1.6.

Рекомендуем запускать проект через виртуальное окружение.

1. Поставьте пакетный менеджер Питона и менеджер виртуальных окружений Питона

        sudo apt-get install python3-setuptools
        sudo pip install virtualenv

3. Склонируйте репозиторий проекта, перейдите в него, создайте виртуальное окружение

        git clone https://github.com/vpavlenko/matprazdnik.git
        cd matprazdnik
        virtualenv-3.3 venv

4. Активируйте виртуальное окружение и установите зависимости проекта

        source venv/bin/activate
        
5. Установите зависимости

        pip install -r requirements.txt

5. Создайте базу данных. При создании выберите `yes` и задайте логин и пароль администратора. Почту оставьте пустой (она ни на что не влияет)

        python3 manage.py syncdb

6. Запустите сервер разработчика

        python3 manage.py runserver
