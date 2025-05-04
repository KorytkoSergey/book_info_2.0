# Скрипты для разворачивания Базы данных PostgreSQL
## Уточнения по БД
- Скрипты накатываем согласно порядку, так как они имеют завимости
- Скрипты содержат первичные тестовые данные для отладки. 
- БД нормализованна, поэтому для внесения новых данных нужно использовать временные таблицы: shelf.temp_table_writers, shelf.temp_table_publish, shelf.temp_table_book
- При необходимости можно сделать временные таблицы для других постоянных таблиц. Перед работой с БД лучше изучить скрипты(комментарии есть)

```
-- таблица - словарь, содержит ключи - страны. Страны происхождения писателей и возможно еще для чего.
CREATE TABLE shelf.nation (
    nation_id SERIAL PRIMARY KEY,
    country VARCHAR(255) NOT null UNIQUE 
);

-- заполняем таблицу nation первыми странами. 
insert into shelf.nation (country)
values 
('Австралия'), ('Австрия'), ('Аргентина'), ('Бельгия'), ('Бразилия'),
('Великобритания'), ('Венгрия'), ('Вьетнам'), ('Германия'), ('Греция'),
('Дания'), ('Египет'), ('Израиль'), ('Индия'), ('Индонезия'),
('Ирландия'), ('Исландия'), ('Испания'), ('Италия'), ('Казахстан'),
('Канада'), ('Катар'), ('Кения'), ('Кипр'), ('Китай'),
('Колумбия'), ('Латвия'), ('Литва'), ('Люксембург'), ('Мексика'),
('Молдавия'), ('Нидерланды'), ('Новая Зеландия'), ('Норвегия'), ('ОАЭ'),
('Перу'), ('Польша'), ('Португалия'), ('Россия'), ('Румыния'),
('Саудовская Аравия'), ('Сербия'), ('Сингапур'), ('Словакия'), ('Словения'),
('США'), ('Таиланд'), ('Турция'), ('Украина'), ('Франция'),
('Чехия'), ('Швейцария'), ('Швеция'), ('ЮАР'), ('Япония');

-- таблица - словарь, содержит ключи - языки. Языки, на которых написаны книги и возможно еще для чего.
create table shelf.lang (
	lang_id SERIAL PRIMARY key,
	language varchar(255)
	);

-- заполняем таблицу lang первыми странами. 
insert into shelf.lang (language)
values 
('Русский'), ('Английский'), ('Немецкий'), ('Французский'), ('Испанский'),  
('Итальянский'), ('Португальский'), ('Китайский'), ('Японский'), ('Корейский'),  
('Арабский'), ('Хинди'), ('Бенгальский'), ('Турецкий'), ('Вьетнамский'),  
('Индонезийский'), ('Тайский'), ('Персидский'), ('Греческий'), ('Польский'),  
('Чешский'), ('Словацкий'), ('Венгерский'), ('Румынский'), ('Украинский'),  
('Белорусский'), ('Казахский'), ('Узбекский'), ('Таджикский'), ('Грузинский'),  
('Армянский'), ('Азербайджанский'), ('Литовский'), ('Латышский'), ('Эстонский'),  
('Финский'), ('Шведский'), ('Норвежский'), ('Датский'), ('Исландский'),  
('Сербский'), ('Хорватский'), ('Словенский'), ('Македонский'), ('Болгарский'),  
('Албанский'), ('Башкирский'), ('Татарский'), ('Чувашский'), ('Монгольский');

-- таблица справочник по жанрам
create table shelf.genre (
	genre_id SERIAL primary key,
	genre_name varchar(255)
	);

-- заполняем таблицу тестовыми жанрами
INSERT INTO shelf.genre (genre_name)  
VALUES  
('Детектив'),  
('Фантастика'),  
('Сказка'),  
('Роман'),  
('Приключения'),  
('Триллер'),  
('Фэнтези'),  
('Исторический роман'),  
('Биография'),  
('Психология'),  
('Научная литература'),  
('Саморазвитие'),  
('Хоррор'),  
('Поэзия'),  
('Драма'),  
('Комедия'),  
('Мистика'),  
('Научная фантастика'),  
('Классика'),  
('Современная литература');  


-- таблица справочник по издательствам
create table shelf.publish (
	publish_id serial primary key,
	publish_name varchar(255),
	country integer,
	foreign key (country) references shelf.nation(nation_id) on delete set null
	);

-- заполняем таблицу тестовыми издательствами
insert into shelf.publish (publish_name, country)
values
('Дрофа', 94), ('Колесо и Крест', 103);

-- Таблица писателей
CREATE TABLE shelf.writers (
    writer_id SERIAL PRIMARY KEY,
    last_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    second_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    nationality INTEGER,  -- Должно быть INTEGER!
    info TEXT,
    FOREIGN KEY (nationality) REFERENCES shelf.nation(nation_id) ON DELETE SET NULL
);

-- Временная таблица для писателей(используется для загрузки)
CREATE TABLE shelf.temp_table_writers (
    last_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    second_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    nationality VARCHAR(255), -- Название страны (не ID)
    info TEXT
);

-- перегоняем из временной таблицы в основную
INSERT INTO shelf.writers (last_name, name, second_name, birth_date, nationality, info)
SELECT
    tt.last_name,
    tt.name,
    tt.second_name,
    tt.birth_date,
    n.nation_id,  -- Теперь записываем числовой ID страны
    tt.info
FROM shelf.temp_table_writers tt
INNER JOIN shelf.nation n ON tt.nationality = n.country; -- Джойним по названию страны

-- перед заливкой из временной таблицы в постояную, нужно обновить словарь со странами
INSERT INTO shelf.nation (country)
SELECT DISTINCT nationality
FROM shelf.temp_table_writers
ON CONFLICT (country) 
DO UPDATE SET country = excluded.country;


-- создаем таблицу для книг
create table shelf.book (
	book_id serial primary key,
	book_name varchar(255) not null,
	date_publish integer not null,
	language integer,
	publish integer,
	writer integer,
	genre integer,
	foreign key (language) references shelf.lang (lang_id) on delete set null, 
	foreign key (publish) references shelf.publish (publish_id) on delete set null,
	foreign key (writer) references shelf.writers (writer_id) on delete set null,
	foreign key (genre) references shelf.genre (genre_id) on delete set null);

-- первые тестовые данные для таблицы book
insert into shelf.book (book_name, date_publish , language, publish, writer, genre)
values 
	('Колобок', '1876', 1, 1, 174, 1);

-- словарь для статуса работника библиотеки
create table shelf.status_worker (
	status_id serial primary key,
	status varchar(255) not null
	);

-- заполняем словарь статусов работников
insert into shelf.status_worker (status)
values 
	('Работает'), ('Уволен'), ('Отпуск'), ('Больничный');

-- таблица читатели
create table shelf.readers (
	reader_id serial primary key,
	surname varchar(255),
	name varchar(255),
	second_name varchar(255),
	aboniment integer not null,
	active_aboniment bool,
	birth_date DATE NOT NULL,             -- Дата рождения
    phone_number VARCHAR(20) UNIQUE,      -- Телефон (уникальный)
    email VARCHAR(255) UNIQUE,            -- Email (уникальный, для уведомлений)
    address TEXT,                          -- Адрес проживания
    registration_date TIMESTAMP DEFAULT NOW()
	);

-- заполнение таблицы читателей
INSERT INTO shelf.readers (surname, name, second_name, aboniment, active_aboniment, birth_date, phone_number, email, address)  
VALUES  
    ('Иванов', 'Алексей', 'Сергеевич', '4568254', true, '1990-05-12', '+79876543210', 'ivanov.alex@mail.ru', 'Москва, ул. Ленина, д. 10'),  
    ('Петров', 'Игорь', 'Андреевич', '45621458', false, '1985-09-22', '+79161234567', 'petrov.igor@gmail.com', 'Санкт-Петербург, Невский пр., д. 50'),  
    ('Сидорова', 'Мария', 'Викторовна', '74185296', true, '1995-07-15', '+79234567890', 'maria.sid@gmail.com', 'Казань, ул. Баумана, д. 3');  


-- таблица словарь должностей работников
create table shelf.roles (
	role_id serial primary key,
	role varchar(255)
	);

-- заполняем таблицу с должностяи работников
insert into shelf.roles (role)
values 
	('Старший библиотекарь'), 
	('Младший библиотекарь'), 
	('Директор'), 
	('Стажер');

-- таблица сотрудников
create table shelf.workers(
	worker_id serial primary key,
	surname varchar(255),
	name varchar(255),
	second_name varchar(255),
	role integer,                    -- ссылаемся на таблицу roles, чтобы определить должность
	status integer,                       -- ссыаемся на таблицу status_worker чтобы опредилить статус работника
	birth_date DATE NOT NULL,             -- Дата рождения
    phone_number VARCHAR(20) UNIQUE,      -- Телефон (уникальный)
    email VARCHAR(255) UNIQUE,            -- Email (уникальный, для уведомлений)
    address TEXT,
    foreign key (role) references shelf.roles(role_id),
    foreign key (status) references shelf.status_worker(status_id)
	);

-- заполняем таблицу работников
insert into shelf.workers (surname, name, second_name, birth_date, phone_number, email, address)
values 
	('Иванов', 'Иван', 'Иванович', '1990-12-01', '77705874212', 'gfddgg@mai.com', 'Алматы, дом 10');

-- таблица историчности взятие/сдачи книги
create table shelf.history (
	history_id serial primary key,
	reader_id integer,
	book_id integer,
	worker_id integer,
	borrow_date timestamp default now(),
	return_date timestamp,
	foreign key (reader_id) references shelf.readers(reader_id),
	foreign key (worker_id) references shelf.workers(worker_id),
	foreign key (book_id) references shelf.book(book_id)
	);

-- таблицу заполняем историчности
insert into shelf.history (reader_id, book_id, worker_id, borrow_date, return_date)
values 
	(1, 3, 1, '2025-02-12', '2025-03-01');

------------------------------------------------------------------------------------------------------------------
-- Временная таблица для издательства(используется для загрузки)
CREATE TABLE shelf.temp_table_publish (
    name VARCHAR(255) NOT NULL,
    nationality VARCHAR(255) -- Название страны (не ID)
);

-- перегоняем из временной таблицы в основную
INSERT INTO shelf.publish (publish_name, country)
SELECT
    tt.name,
    n.nation_id  -- Теперь записываем числовой ID страны
FROM shelf.temp_table_publish tt
INNER JOIN shelf.nation n ON tt.nationality = n.country; -- Джойним по названию страны

-- перед заливкой из временной таблицы в постояную, нужно обновить словарь со странами
INSERT INTO shelf.nation (country)
SELECT DISTINCT nationality
FROM shelf.temp_table_publish
ON CONFLICT (country) 
DO UPDATE SET country = excluded.country;
-----------------------------------------------------------------------------------------------------------------------
-- Временная таблица для книг(используется для загрузки) (есть проблема потенциальная с писателями и с издательсвами. 
-- Сложно обновлять старые таблицы, нужно над запросом, пока не углубляюсь, поэтому не трогаю.)
CREATE TABLE shelf.temp_table_book (
	book_name varchar(255) not null,
	date_publish varchar(255),
	language varchar(255),
	publish varchar(255),
	writer varchar(255),
	genre varchar(255)
);

-- перегоняем из временной таблицы в основную
INSERT INTO shelf.book (book_name, date_publish, language, publish, writer, genre)
SELECT
    tt.book_name,
    tt.date_publish,
    l.lang_id,
    p.publish_id,
    tt.writer,  
    g.genre_id
FROM shelf.temp_table_book tt
INNER JOIN shelf.lang l ON tt.language = l.language -- Джойним по языку
INNER JOIN shelf.publish p ON tt.publish = p.publish_name -- Джойним по названию издательства
INNER JOIN shelf.genre g ON tt.genre = g.genre_name; -- Джойним по названию страны

-- перед заливкой из временной таблицы в постояную, нужно обновить словарь с языками
INSERT INTO shelf.lang (language)
SELECT DISTINCT language
FROM shelf.temp_table_book
ON CONFLICT (language) 
DO UPDATE SET language = excluded.language;

-- перед заливкой из временной таблицы в постояную, нужно обновить словарь со жанрами
INSERT INTO shelf.genre (genre_name)
SELECT DISTINCT genre
FROM shelf.temp_table_book
ON CONFLICT (genre_name) 
DO UPDATE SET genre_name = excluded.genre_name;
```