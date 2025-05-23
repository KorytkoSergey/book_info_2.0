**PUT** `/writers/int:writer_id`

Типы ошибок:

| Код | Название | Описание |
| --- | --- | --- |
| 200 | Писатель успешно обновлён | Успешный запрос |
| 400 | error | Ошибка общего типа. Проблема может быть как на стороне пользователя, так и на стороне сервера. |
| 404 | Писатель не найден | Вероятно не верный id или такого писателя нет в БД. |

### Описание

Изменяет информацию/данные писателя.

### Параметры запроса json

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| last_name | string | Фамилия писателя | Чехов |
| name | string | Имя писателя | Сашак |
| second_name | string | Отчество писателя | Антон |
| birth_date | date | Дата рождения. Формат `year-mm-dd`  | 1990-05-12 |
| nationality | int | id национальности из таблицы shelf.nation (nation_id) | 58 |
| info | text | Краткая биография или информация о писателе. Формате текста, поэтому ограничений нет | Где то родился, а где то пригодился! |

### Пример тела json

```bash
{
    "last_name": "Чехов",
    "name": "Антон",
    "second_name": "Павлович",
    "birth_date": "1860-01-29",
    "nationality": 94,
    "info": "Все делаем своими руками. Мансарда"
}
```

Пример запроса cURL

```bash
curl --silent --location --request PUT '[http://127.0.0.1:5000/readers](http://127.0.0.1:5000/readers/7)' 
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
    "message": "Писатель успешно обновлён",
    "writer": {
        "birth_date": "Sun, 29 Jan 1860 00:00:00 GMT",
        "info": "Все делаем своими руками. Мансарда",
        "last_name": "Чехов",
        "name": "Антон",
        "nationality": 94,
        "second_name": "Павлович",
        "writer_id": 176
    }
}
```
# Swagger
<iframe
  src="http://127.0.0.1:8000/swagger-ui/put_writers.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>