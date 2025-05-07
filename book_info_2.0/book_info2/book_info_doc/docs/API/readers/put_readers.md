## Изменение читателя

**PUT** `/readers/<int:reader_id>`

### 🔹 Описание

Меняет информацию по конкретному читателю

### 🔹 Параметры запроса json

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| surname | string | Фамилия читателя | Корытков |
| name | string | Имя читателя | Алексей |
| second_name | string | Отчество читателя | Сергеевич |
| aboniment | int8 | Номер абонемента. | 45168254 |
| active_aboniment | bool | Активен ли абонемент. Принимает значения `true` или `false` | true |
| birth_date | date | Дата рождения. Формат `year-mm-dd`  | 1990-05-12 |
| phone_number | string | Номер телефона читателя | +79876853210 |
| email | string | Адрес почты читателя | [ivanqov.alex@mail.ru](mailto:ivanqov.alex@mail.ru) |
| address | text | Адрес. Формате текста, поэтому ограничений нет | Казань, ул. Баумана, д. 3 |

### 🔹 Пример тела json

```bash
{
  "surname": "Корытко",
  "name": "Алексей",
  "second_name": "Сергеевич",
  "aboniment": 45168254,
  "active_aboniment": true,
  "birth_date": "1990-05-12",
  "phone_number": "+79876853210",
  "email": "ivanqov.alex@mail.ru",
  "address": "Казань, ул. Баумана, д. 3"
}
```

Пример запроса cURL

```bash
curl --silent --location --request PUT 'http://127.0.0.1:5000/readers/7' 
--header 'Authorization: Bearer <ваш токен>'
--header 'Content-Type: application/json' `
--data-raw '{
"surname": "Корытко",
"name": "Алексей",
"second_name": "Сергеевич",
"aboniment": 45168254,
"active_aboniment": true,
"birth_date": "1990-05-12",
"phone_number": "+79876853210",
"email": "[ivanqov.alex@mail.ru](mailto:ivanqov.alex@mail.ru)",
"address": "Казань, ул. Баумана, д. 3"
}'
```

Пример ответа

```bash
 {
    "message": "Читатель успешно обновлён",
    "reader": {
        "aboniment": 45168254,
        "active_aboniment": true,
        "address": "Казань, ул. Баумана, д. 3",
        "birth_date": "Sat, 12 May 1990 00:00:00 GMT",
        "email": "ivanqov.alex@mail.ru",
        "name": "Алексей",
        "phone_number": "+79876853210",
        "reader_id": 7,
        "registration_date": "Mon, 24 Mar 2025 17:00:15 GMT",
        "second_name": "Сергеевич",
        "surname": "Корытко"
    }
}
```