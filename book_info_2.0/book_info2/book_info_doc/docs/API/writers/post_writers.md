**POST** `/writers`

Типы ошибок:

| Код | Название | Описание |
| --- | --- | --- |
| 201 | Писатель добавлен | Успешный запрос |
| 400 | error | Ошибка общего типа. Проблема может быть как на стороне пользователя, так и на стороне сервера. |

### Описание

Добавляет нового писателя

### Параметры запроса json

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| last_name | string | Фамилия писателя | Котовcкий |
| name | string | Имя писателя | Сашак |
| second_name | string | Отчество писателя | Петрович |
| birth_date | date | Дата рождения. Формат `year-mm-dd`  | 1990-05-12 |
| nationality | int | id национальности из таблицы shelf.nation (nation_id) | 58 |
| info | text | Краткая биография или информация о писателе. Формате текста, поэтому ограничений нет | Где то родился, а где то пригодился! |

### Пример тела json

```bash
{
"last_name": "Котовcкий",
"name": "Сашак",
"second_name": "Петрович",
"birth_date": "1928-09-19",
"nationality": 58,
"info": "Где то родился, а где то пригодился!"
}
```

Пример запроса **cURL**

```bash
curl --silent --location --request POST '[http://127.0.0.1:5000/readers](http://127.0.0.1:5000/readers/7)' 
--header 'Authorization: Bearer <ваш токен>'
--header 'Content-Type: application/json' `
--data '{
  "last_name": "Котовcкий",
  "name": "Сашак",
  "second_name": "Петрович",
  "birth_date": "1928-09-19",
  "nationality": 58,
  "info": "Где то родился, а где то пригодился!"
}
'
```

Пример ответа

```bash
 {
    "message": "Писатель добавлен"
}
```
# Swagger
<iframe
  src="http://127.0.0.1:8000/swagger-ui/post_writers.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>