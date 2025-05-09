### Документация API XML-сервиса платежей

## Endpoint

```
POST /bank
Content-Type: application/xml

```

## Общее описание

Сервис принимает XML-запросы с атрибутом `type` в корневом элементе `<request>` и обрабатывает их по трем сценариям:

- Проверка счета (`check`)
- Подтверждение платежа (`confirm`)
- Уведомление о статусе (`notify`)

Ответ также формируется в формате XML.

---

## Тип запроса: `check`

### Пример запроса:

```xml
<request type="check">
    <account>1234567890</account>
    <amount>1500.00</amount>
    <currency>KZT</currency>
</request>

```

### Описание параметров:

| Тег | Тип | Обязательный | Описание |
| --- | --- | --- | --- |
| `account` | string | Да | Номер счёта |
| `amount` | decimal | Да | Сумма к оплате |
| `currency` | string | Да | Валюта (ISO 4217, напр. KZT) |

### Ответ:

```xml
<response>
    <status>ok</status>
    <message>Account found. Ready to accept payment.</message>
</response>

```

---

## Тип запроса: `confirm`

### Пример запроса:

```xml
<request type="confirm">
    <transaction_id>TXN001</transaction_id>
    <amount>1500.00</amount>
</request>

```

### Описание параметров:

| Тег | Тип | Обязательный | Описание |
| --- | --- | --- | --- |
| `transaction_id` | string | Да | Уникальный ID транзакции |
| `amount` | decimal | Да | Сумма платежа |

### Ответ:

```xml
<response>
    <status>confirmed</status>
    <message>Payment confirmed</message>
</response>

```

---

## Тип запроса: `notify`

### Пример запроса:

```xml
<request type="notify">
    <transaction_id>TXN001</transaction_id>
    <status>success</status>
    <timestamp>2025-05-09T13:00:00Z</timestamp>
</request>

```

### Описание параметров:

| Тег | Тип | Обязательный | Описание |
| --- | --- | --- | --- |
| `transaction_id` | string | Да | Уникальный ID транзакции |
| `status` | string | Да | Статус (`success`, `failed`) |
| `timestamp` | datetime | Да | Время события в ISO 8601 |

### Ответ:

```xml
<response>
    <status>received</status>
    <message>Notification accepted</message>
</response>

```

---

## Ошибки

### Неверный `type`:

```xml
<response>
    <status>error</status>
    <message>Unknown request type</message>
</response>

```

### Невалидный XML:

```xml
<response>
    <status>error</status>
    <message>Invalid XML format</message>
</response>

```

---

## Прочее

- Все значения чувствительны к регистру.
- Ответ всегда возвращается в формате XML с `Content-Type: application/xml`.
- Запросы должны отправляться методом `POST`.