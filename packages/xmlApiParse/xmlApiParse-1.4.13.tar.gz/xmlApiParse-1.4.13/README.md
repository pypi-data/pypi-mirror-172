## Первичная настройка (создание виртуального окружения и получение зависимостей)

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install poetry
poetry install
```

## Примеры находятся в папке Example
* get_auth.py - служит для подключение в API
* get_colleciton.py - Получает все коллекций или конкретную коллекцию
* get_employees.py - Все сотрудники
* get_menu_items - Все блюда и поиск определенных блюд
* get_menu.py - Все заказанные блюда их идентификации и цены
* get_order_list - Все заказы
* get_order_lines - Строка заказов
* get_restaurants - Рестораны
* get_waiter_list.py - id и код всех официантов

## Ссылка на модуль: <a href="https://pypi.org/project/xmlApiParse/" title="Go to Pypi ">Click here</a>
 <img src="https://raw.githubusercontent.com/github/explore/666de02829613e0244e9441b114edb85781e972c/topics/pip/pip.png" height="150" width="150"/>

## Выгрузка новой версии
* В файле setup.py обновляем номер версии: `version="2.2.4"`
* Выполняем скрипт:
```bash
chmod +x deploy.sh
source env/bin/activate
./deploy.sh
```