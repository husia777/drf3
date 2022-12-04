# DRF Project 2

<h3>Backup БД файл postgres_localhost-2022_11_21_16_05_34-dump.sql</h3>

<h3>Команды создания и заполнения таблиц </h3>
./manage.py makemigrations ads
<br>
./manage.py migrate
<br>
./manage.py load_data
<br>

<h3>шаг 1</h3> 
URL для создания пользователя 
http://127.0.0.1:8000/user/create/

{
"first_name":"Новый пользователь3",
"last_name":"1",
"username":"3",
"password":"3",
"location":["1", "2", "3"],
"role":"user",
"age":"22"
}
}<h4> проверка обновления и создания юзера</h4>


<h3>шаг 2</h3> 
URL для проверки 2 шага
http://127.0.0.1:8000/location/

<h3>шаг 3</h3>  
1 http://127.0.0.1:8000/ad?cat=1<br>
2 http://127.0.0.1:8000/ad?text=принципы<br>
3 http://127.0.0.1:8000/ad?location=Москва<br>


<h3>шаг 4</h3> 

http://127.0.0.1:8000/ad?price_from=100&price_to=100 
<h3>шаг 5 </h3>
Чтобы получить JWT токен для пользователя введите POST запрос и отправьте JSON данные
http://127.0.0.1:8000/token/
{
"username":"husia777",
"password":"sasa222"
}
Для refresh http://127.0.0.1:8000/token/refresh/

для обычного токена
http://127.0.0.1:8000/login/
{   
"username":"husia777",
"password":"sasa222"
}
для выхода
http://127.0.0.1:8000/logout/
и в Authorization ввести Token <имя токена>

чтобы получить данные о каком то именно товаре
http://127.0.0.1:8000/ad/1/
и в Authorization ввести Bearer <имя токена>

для создания подборки 
http://127.0.0.1:8000/compilation/create/
{
    "name":"обновленная подборка",
    "owner":"19",
    "items":[1,2,3]
}