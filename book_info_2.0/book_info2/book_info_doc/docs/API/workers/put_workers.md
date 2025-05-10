**PUT** `/workers/<int:worker_id>`

Типы ошибок:

| Код | Название | Описание |
| --- | --- | --- |
| 200 | Работник успешно обновлён | Успешный запрос |
| 400 | error | Ошибка общего типа. Проблема может быть как на стороне пользователя, так и на стороне сервера. |
| 404 | Работник не найден | Данного работника нет в системе |

### Описание

Изменяет информацию по работнику библиотеки через его id

### Параметры запроса  json

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| surname | string | Фамилия сотрудника | Собакин |
| name | string | Имя сотрудника | Иван |
| second_name | string | Отчество сотрудника | Дмитриевич |
| role | int | Значение роли сотрудника id из БД shelf.roles | 3 |
| status | int | Значение статуса(работает или уволен или др.)сотрудника id из БД shelf.status | 3 |
| birth_date | date | Дата рождения в формате `years-mm-dd` | 1997-02-21 |
| phone_number | string | Номер телефона | +773241564589 |
| email | string | Адрес электронной почты | [dfghj@fghj.com](mailto:dfghj@fghj.com) |
| address | text | Адрес сотрудника | dfghjklfghj,fgbnm |

### Пример json

```bash
{
    "surname": "Собакин",
    "name": "Иван",
    "second_name": "Дмитриевич",
    "role": 3,
    "status": 3,
    "birth_date": "1997-02-21",
    "phone_number": "+773241564589",
    "email": "dfghj@fghj.com",
    "address": "dfghjklfghj,fgbnm"
}
```

Пример запроса **cURL**

```bash
curl --silent --location --request PUT 'http://127.0.0.1:5000/workers/32' `
--header 'Authorization: Bearer <ваш токен>' `
--header 'Content-Type: application/json' `
--data-raw '{
    "surname": "Собакин",
    "name": "Иван",
    "second_name": "Дмитриевич",
    "role": 3,
    "status": 3,
    "birth_date": "1997-02-21",
    "phone_number": "+773241564589",
    "email": "dfghj@fghj.com",
    "address": "dfghjklfghj,fgbnm"
}'
```

Пример ответа

```bash
{
    "message": "Работник успешно обновлён",
    "worker": {
        "address": "dfghjklfghj,fgbnm",
        "birth_date": "Fri, 21 Feb 1997 00:00:00 GMT",
        "email": "dfghj@fghj.com",
        "name": "Иван",
        "phone_number": "+773241564589",
        "role": 3,
        "second_name": "Иван",
        "status": 3,
        "surname": "Собакин",
        "worker_id": 32
    }
}
```