**GET** `/workers`

### Описание

Возвращает информацию по сотруднику библиотеки. Можем фильтровать по имени, статусу(работает или уволен), id или должности.

### Параметры запроса (Query)

| Параметр | Тип | Описание | Пример запроса |
| --- | --- | --- | --- |
| worker_id | int | id работника, который нас интересует | 23 |
| worker_name | string | Фильтр по имени сотрудника 
Важно! Вместо пробела используем подчеркивание  _ | Иванов_Иван_Алексеевич |
| status | string | Фильтр по статусу сотрудника. Возможные статусы: `Работает`, `Уволен`, `Отпуск`, `Больничный`  | Уволен |
| role | string | Фильтр по роле сотрудника. Возможные роли: `Старший библиотекарь`, `Младший библиотекарь`, `Директор`, `Стажер` | Стажер |

### Пример запроса

```bash
GET /workers?role=Стажер
```

Пример запроса HTTP

```bash
GET /workers?role=Стажер HTTP/1.1
Host: 127.0.0.1:5000
Authorization: Bearer {your toker}
```

Пример запроса **cURL**

```bash
curl --silent --location 'http://127.0.0.1:5000/workers?role=Стажер}' `
--header 'Authorization: Bearer {your toker}' | jq
```

Пример ответа

```bash
[
    {
        "address": "г. Тверь",
        "birth_date": "Tue, 11 Oct 1988 00:00:00 GMT",
        "email": "filatov@example.com",
        "phone_number": "789641256",
        "role": "Стажер",
        "status": "Отпуск",
        "worker_id": 30,
        "ФИО Сотрудника": "Филатов Константин Игоревич"
    },
    {
        "address": "г. Казань",
        "birth_date": "Fri, 30 Dec 1983 00:00:00 GMT",
        "email": "ivanov@example.com",
        "phone_number": "789641259",
        "role": "Стажер",
        "status": "Больничный",
        "worker_id": 33,
        "ФИО Сотрудника": "Иванов Дмитрий Алексеевич"
    },
    {
        "address": "г. Новосибирск",
        "birth_date": "Fri, 25 Sep 1992 00:00:00 GMT",
        "email": "grigorieva@example.com",
        "phone_number": "789641262",
        "role": "Стажер",
        "status": "Уволен",
        "worker_id": 36,
        "ФИО Сотрудника": "Григорьева Анна Олеговна"
    }
  ]
```
# Swagger
<iframe
  src="http://127.0.0.1:8000/swagger-ui/get_workers.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>