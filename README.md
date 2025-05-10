# Book Info 2.0

**Book Info 2.0** — это система для управления библиотекой с помощью Django и Telegram-бота. Пользователи могут регистрироваться, искать книги, а сотрудники библиотеки — управлять доступом и проверять наличие книг.

## Документация проекта 

https://korytkosergey.github.io/book_info_2.0/

## Функциональность

### Веб-приложение (Flask)
- Регистрация и аутентификация пользователей
- Разделение ролей: пользователь / сотрудник
- Каталог книг и поиск

## Стек технологий

- Python 3.10+
- Flask
- PostgreSQL

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/KorytkoSergey/book_info_2.0.git
cd book_info_2.0
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```
### 4. Развертывание БД
Скрипты, схема описаны в этом разделе документации https://korytkosergey.github.io/book_info_2.0/db/schema/


### 5. Запуск сервера

```bash
python app.py
````

## Структура проекта

```
book_info_2.0/book_info2
├── book_info2
    ├── book_info_doc/      # Документация проекта
    ├── app.py              # Основной API, в котором описана логика обработки
    ├── bank_stub.py        # API оплаты
    ├── models.py           # Модели для БД. Файл опциональный, так как используются скрипты SQL для разворачивания БД
    ├── query.py            # SQL скрипты 
├── requirements.txt    # Зависимости
```

## Контрибьюторам

1. Сделайте форк проекта
2. Создайте ветку `feature/ваша-функция`
3. Отправьте pull-request с описанием изменений

## Лицензия

Проект распространяется под лицензией MIT.
