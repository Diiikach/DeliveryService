Delivery Service - это REST-API сервер для управления курьерами и назначения им заказов.
<h1>Instalation guide:</h1>

```git clone https://github.com/mikacha/DeliveryService```<br>
```virtualenv env```<br>
```source env/bin/activate```<br>
```cd DeliveryService/Delivery```<br>
```cd DeliveryService/Delivery```<br>
```pip3 install -r requirements.txt```<br>

<h3>Для того,чтобы запустить сервер - необходимо провести миграции python объектов к базе данных.</h3><br>
<h4>$ python3 manage.py makemigrations</h4><br>
<h4>$ python3 manage.py migrate</h4><br>
В settings.py неоходимо добавить в ALLOWED_HOSTS строку, состоящую из вашего IP, на котором вы намерены запустись сервер<br>
$ python3 manage.py runserver 0.0.0.0:8000<br>
Сервер будет запущен на 8000 порту внешнего ip адреса.
<h3>Для запуска тестов - необходимо запустить:</h3><br>
	<h4>$ python3 manage.py test.</h4>
	<br>
	
<h1>Информация о проекте:</h1>
Проект написан с использованием фреймворка django. Бизнес логика размещена в слое models и в слое services.
Роль контроллера выполняет слой views и слой urls.
	
<h1>Рекомендации по использованию:<h1>
	Следует использовать сервер gunicorn для обработки wsgi запросов, поскольку тестировочный сервер Django не присобослен для нагрузки.
	
