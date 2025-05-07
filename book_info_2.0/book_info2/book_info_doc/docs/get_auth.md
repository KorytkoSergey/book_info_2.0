Пользователи делятся на два типа: <span style="color: purple; font-weight: bold;">admin</span> и <span style="color: green; font-weight: bold;">user</span>. В данный момент разделение условно. Пароль и пользователь указывается внутри скрипта. 
Типы ошибок: 

| Код | Название                  | Описание                                                              |
|-----|---------------------------|-----------------------------------------------------------------------|
| 200 | OK                        | Успешный запрос                                                       |
| 401 | Invalid credentials       | Стоит проверить логин и пароль                                        |
| 403 | Forbidden                 | Доступ запрещён. Неверный токен.                                      |



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

## Авторизация

Делаем запрос на адрес `/login`  через метод [**POST**]

```
[post]
http://127.0.0.1:5000/login
```

Для <span style="color: orange; font-weight: bold;">Postman</span> в теле (Body) указываем логин пользователя. 

Пример в <span style="color: orange; font-weight: bold;">Postman</span> для пользователя <span style="color: green; font-weight: bold;">user</span>

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

Ответ в <span style="color: orange; font-weight: bold;">Postman</span> и через **cURL** будет один

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzAwNzMwNCwianRpIjoiZmEyZjFiNDItMzE0Zi00OWZmLTgwY2ItOTJiNDhjOGU4ZjA5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NDMwMDczMDQsImNzcmYiOiIzOWY5MmU3MS1jMTViLTRlMDktODExYi0xMGJiNTE1MGE1OTYiLCJleHAiOjE3NDMwMDgyMDQsInJvbGUiOiJ1c2VyIn0.cwlyka2IthN_OujFKkjpkDUGaCNbTcuBFzz2ZMLWXX4"
}
```

## Аунтификация

Подтверждение верного токена для пользователя одна для <span style="color: purple; font-weight: bold;">admin</span> и <span style="color: green; font-weight: bold;">user</span>

Делаем [**GET**] запрос на `/user` 

В <span style="color: orange; font-weight: bold;">Postman</span> указываем в заголовках (Headers) 

```
Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzAwNzMwNCwianRpIjoiZmEyZjFiNDItMzE0Zi00OWZmLTgwY2ItOTJiNDhjOGU4ZjA5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NDMwMDczMDQsImNzcmYiOiIzOWY5MmU3MS1jMTViLTRlMDktODExYi0xMGJiNTE1MGE1OTYiLCJleHAiOjE3NDMwMDgyMDQsInJvbGUiOiJ1c2VyIn0.cwlyka2IthN_OujFKkjpkDUGaCNbTcuBFzz2ZMLWXX4
```

Пример для <span style="color: orange; font-weight: bold;">Postman</span> 

![Image title](https://raw.githubusercontent.com/KorytkoSergey/book_info_2.0/main/book_info_2.0/book_info2/book_info_doc/docs/images/auth_postman.png){ loading=lazy }

Пример запроса через **cURL** PowerShell 

```
curl --silent --location 'http://127.0.0.1:5000/user' `
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzAwOTM5OCwianRpIjoiNjk2NzU5YTUtMjAzOC00NTIxLWE0MDEtOTg2OGRjMzllMjEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NDMwMDkzOTgsImNzcmYiOiJjYzg5ODFjOC1jMzJiLTRiZmEtOTA3YS04NjIyNzlmMjU4NDAiLCJleHAiOjE3NDMwMTAyOTgsInJvbGUiOiJ1c2VyIn0.F0TaEJPvCDwMedvE6yjv_rQlvaJ7SaMiTZPGFTTniq0'
```

Ответ в <span style="color: orange; font-weight: bold;">Postman</span> и через **cURL** будет зависеть от типа пользователя

Для <span style="color: purple; font-weight: bold;">admin</span> 

```
{
    "msg": "Welcome, user!"
}
```

Для <span style="color: green; font-weight: bold;">user</span>

```
{
    "msg": "Welcome, user!"
}
```

Дальнейшие запросы проводиться с внесенным токеном в заголовке (Headers)

```
Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzAwNzMwNCwianRpIjoiZmEyZjFiNDItMzE0Zi00OWZmLTgwY2ItOTJiNDhjOGU4ZjA5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NDMwMDczMDQsImNzcmYiOiIzOWY5MmU3MS1jMTViLTRlMDktODExYi0xMGJiNTE1MGE1OTYiLCJleHAiOjE3NDMwMDgyMDQsInJvbGUiOiJ1c2VyIn0.cwlyka2IthN_OujFKkjpkDUGaCNbTcuBFzz2ZMLWXX4
```

