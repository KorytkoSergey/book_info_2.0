**POST** `/books`

Типы ошибок:

| Код | Название | Описание |
| --- | --- | --- |
| 201 | Книга добавлена | Успешный запрос |
| 400 | error | Ошибка общего типа. Проблема может быть как на стороне пользователя, так и на стороне сервера. |

### Описание

Добавляет в базу данных книгу. 

### Параметры тела json

Все параметры указываем в единственном числе. 

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| book_name | string | Название книги | Маями Хит |
| date_publish | int | Дата издания | 1876 |
| language | int | Язык, на котором напечатана книга. Указывать необходимо id языка из таблицы shelf.lang | 18 |
| publish | int | Издательство, в котором напечатана книга. Указывать необходимо id издательства из таблицы shelf.publish | 18 |
| writer | int | Писатель, который написал книгу. Указывать необходимо id издательства из таблицы shelf.writers | 200 |
| genre | int | Жанр, в котором напечатана книга. Указывать необходимо id издательства из таблицы shelf.publish | 13 |

### Пример запроса

Пример самого json

```
{
"book_name": "Маями Хит",
"date_publish": 1974,
"language": 18,
"publish": 18,
"writer": 200,
"genre": 13
}
```

Пример запроса **cURL**

```
curl -X POST http://localhost:5000/books \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <ваш_JWT_токен>" \
-d '{
"book_name": "Маями Хит",
"date_publish": 1974,
"language": 18,
"publish": 18,
"writer": 200,
"genre": 13
}' | jq

```

Пример ответа

```
{
    "book_info": {
        "book_id": 207,
        "book_name": "Маями Хит",
        "date_publish": 1974,
        "genre": 13,
        "language": 18,
        "publish": 18,
        "writer": 200
    },
    "message": "Книга добавлена"
}
```
# Swagger
<iframe
  src="http://127.0.0.1:8000/swagger-ui/post_books.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>