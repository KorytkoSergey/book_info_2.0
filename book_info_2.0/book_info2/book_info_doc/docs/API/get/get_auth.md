Пользователи делятся на два типа: <span style="color: purple; font-weight: bold;">admin</span> и <span style="color: green; font-weight: bold;">user</span>. В данный момент разделение условно. Пароль и пользователь указывается внутри скрипта. 

Тестовые логин и пароль для ролей:
<span style="color: purple; font-weight: bold;">admin</span>

```
{
    "username": "admin",
    "password": "1234"
}
```

<span style="color: green; font-weight: bold;">user</span>

```
{
    "username": "user",
    "password": "5678"
}
```

### Авторизация

Делаем запрос на адрес `/login`  через метод [**POST**]

```
[post]
http://127.0.0.1:5000/login
```

Для Postman в теле (Body) указываем логин пользователя. 

Пример в Postman для пользователя user

![Image title](https://raw.githubusercontent.com/KorytkoSergey/book_info_2.0/main/book_info_2.0/book_info2/book_info_doc/docs/images/post_auth_user.png){ loading=lazy }

Пример запроса через **cURL** PowerShell 

```
curl --silent --location 'http://127.0.0.1:5000/login' `
--header 'Content-Type: application/json' `
--data '{
    "username": "user",
    "password": "5678"
}'
```

Ответ в Postman и через cURL будет один

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzAwNzMwNCwianRpIjoiZmEyZjFiNDItMzE0Zi00OWZmLTgwY2ItOTJiNDhjOGU4ZjA5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NDMwMDczMDQsImNzcmYiOiIzOWY5MmU3MS1jMTViLTRlMDktODExYi0xMGJiNTE1MGE1OTYiLCJleHAiOjE3NDMwMDgyMDQsInJvbGUiOiJ1c2VyIn0.cwlyka2IthN_OujFKkjpkDUGaCNbTcuBFzz2ZMLWXX4"
}

```