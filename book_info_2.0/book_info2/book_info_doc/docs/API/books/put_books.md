**PUT** `/books/<int:book_id>`
Типы ошибок:

| Код | Название | Описание |
| --- | --- | --- |
| 200 | Книга успешно обновлен | Успешный запрос |
| 404 | Книга не найдена | По `book_id` не найдена книга. Вероятно не верный id или данной книги нет в каталоге. |

### Описание

Исправляет в БД значения по конкретно запрошенной книге. 

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

```bash
{
    "book_name": "Тракторист Иван",
    "date_publish": 1999,
    "language": 5,
    "publish": 30,
    "writer": 309,
    "genre": 5
}
```

Пример запроса **cURL**

```
curl -X POST http://localhost:5000/books \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <ваш_JWT_токен>" \
-d '{
    "book_name": "Тракторист Иван",
    "date_publish": 1999,
    "language": 5,
    "publish": 30,
    "writer": 309,
    "genre": 5
}' | jq

```

Пример ответа

```json
{
    "book": {
        "book_id": 4,
        "book_name": "Тракторист Иван",
        "date_publish": 1999,
        "genre": 5,
        "language": 5,
        "publish": 30,
        "writer": 309
    },
    "message": "Книга успешно обновлена"
}
_______________________________________________
{
    "error": "Книга не найдена"
}
```
# Swagger
<iframe
  src="http://127.0.0.1:8000/swagger-ui/put_books.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>