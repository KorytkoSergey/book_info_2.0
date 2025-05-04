# Основные CRUD команды для БД *book_info*
Данные команды помогут для стартовой настройки и отладки. Также они используются в API. 

```
---------------------------- выводим данные о книге ----------------------------
SELECT 
    b.book_name AS "Название",
    b.date_publish AS "Дата издания",
    l.language AS "Язык",
    p.publish_name AS "Издательство",
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Автора",
    g.genre_name AS "Жанр",
    COALESCE(  -- выводит "Нет читателей", если подзапрос дает NULL
        (SELECT STRING_AGG(r.surname || ' ' || r.name || ' ' || r.second_name, ', ') -- агрегирует читателей из подзапроса, через запятую
         FROM shelf.history h
         JOIN shelf.readers r ON h.reader_id = r.reader_id
         WHERE h.book_id = b.book_id
        ), 'Нет читателей'
    ) AS "Читатели",
    COALESCE(  -- выводит "Нет читателей", если подзапрос дает NULL
        (SELECT STRING_AGG(w.surname || ' ' || w.name || ' ' || w.second_name, ', ') -- агрегирует читателей из подзапроса, через запятую
         FROM shelf.history h
         JOIN shelf.workers w ON h.worker_id = w.worker_id
         WHERE h.book_id = b.book_id
        ), 'Ни кем не выдавалась'
    ) AS "Работник библиотеки",
    (case 
    	when h.return_date is null then 'На руках'
    	else 'В библеотеке'
    end) as "Нахождение" -- условие, которое смотрит на наличие null в таблице history и если книга не возвращена, то ставим статус "На руках"    
FROM shelf.book b
JOIN shelf.lang l ON b.language = l.lang_id
JOIN shelf.publish p ON b.publish = p.publish_id
JOIN shelf.writers w ON b.writer = w.writer_id
JOIN shelf.genre g ON b.genre = g.genre_id
join shelf.history h on b.book_id = h.history_id
where b.book_id = 13;

SELECT json_build_object( -- вывод в форме json
    'Название', b.book_name,
    'Дата издания', b.date_publish,
    'Язык', l.language,
    'Издательство', p.publish_name,
    'Автор', json_build_object(
        'Фамилия', w.last_name,
        'Имя', w.name,
        'Отчество', w.second_name
    ),
    'Жанр', g.genre_name,
    'Читатели', COALESCE(
        (SELECT json_agg(json_build_object(
            'ФИО', r.surname || ' ' || r.name || ' ' || r.second_name,
            'Дата взятия', h.borrow_date,
            'Дата возврата', h.return_date
        ))
        FROM shelf.history h
        JOIN shelf.readers r ON h.reader_id = r.reader_id
        WHERE h.book_id = b.book_id
        ), '[]'::json)  -- Если читателей нет, вернуть пустой массив
) AS book_info
FROM shelf.book b
JOIN shelf.lang l ON b.language = l.lang_id
JOIN shelf.publish p ON b.publish = p.publish_id
JOIN shelf.writers w ON b.writer = w.writer_id
JOIN shelf.genre g ON b.genre = g.genre_id;

---------------------------- выводим данные о читателях ----------------------------
SELECT 
    r.surname || ' ' || r.name || ' ' || r.second_name AS "ФИО Читателя",
    r.aboniment AS "Абонимент",
    r.active_aboniment AS "Действителен абонимент?",
    r.birth_date AS "Дата рождения",
    r.email,
    r.phone_number AS "Номер телефона",
    r.address AS "Адрес",
    COALESCE(  
        (SELECT STRING_AGG(b.book_name, ', ')  
         FROM shelf.history h
         JOIN shelf.book b ON h.book_id = b.book_id
         WHERE h.reader_id = r.reader_id
        ), 'Не брал книг'
    ) AS "Книги на руках"
FROM shelf.readers r;

---------------------------- выводим данные о работниках ----------------------------
select
	w.worker_id,
	w.surname || ' ' || w.name || ' ' || w.second_name AS "ФИО Сотрудника",
	r.role,
	s.status,
	w.birth_date,
	w.phone_number,
	w.email,
	w.address
from shelf.workers w
join shelf.roles r on w.role = r.role_id
join shelf.status_worker s on w.status = s.status_id;

---------------------------- выводим данные о писателях ----------------------------
WITH writers_result AS (
    SELECT
        w.writer_id,
        w.last_name || ' ' || w.name || ' ' || w.second_name AS "FIO",
        w.birth_date,
        CASE
            WHEN q.books_name IS NULL THEN 'Нет книг'
            ELSE q.books_name
        END AS books_name,
        n.country,
        w.info
    FROM shelf.writers w
    JOIN shelf.nation n ON w.nationality = n.nation_id
    LEFT JOIN (
        SELECT
            q.writer,
            STRING_AGG(q.book_name, ', ') AS books_name
        FROM shelf.book q
        GROUP BY q.writer
    ) q ON q.writer = w.writer_id
)
SELECT * FROM writers_result;

---------------------------- добавляем нового писателя ----------------------------
        INSERT INTO shelf.writers (last_name, name, second_name, birth_date, nationality, info)
        VALUES ('Бетменов', 'Максим', 'Олегович', '1921-11-11', 77, 'W Radomsku policjanci w ciągu jednego dnia zatrzymali 4 braci za różne przestępstwa.')
        returning *;
        
---------------------------- добавляем новую книгу ----------------------------
        INSERT INTO shelf.book (book_name, date_publish, language, publish, writer, genre)
        VALUES ('Король говорит', 1921, 6, 18, 200, 13)
        returning *;

---------------------------- добавляем нового читателя ----------------------------
        INSERT INTO shelf.readers (surname, name, second_name, aboniment, active_aboniment, birth_date, phone_number, email, address)
        VALUES ('Ланьков', 'Борис', 'Владимирович', 78852141921, True, '1991-11-11', '+7770242200', 'emao3@email.com', 'Город, Улица, дом и улица 12')
        returning *;


---------------------------- обновление писателя ----------------------------
UPDATE shelf.writers
SET
    last_name = 'Петров',
    name = 'Александр',
    second_name = 'Игоревич',
    birth_date = '1980-05-10',
    nationality = 70,
    info = 'Обновлённая информация о писателе.'
WHERE writer_id = 175
RETURNING *;


---------------------------- обновление книги ----------------------------
UPDATE shelf.book
SET
    book_name = 'Петров Чапаев',
    date_publish = 1754,
    language = 34,
    publish = 2,
    writer = 174,
    genre = 32
WHERE book_id = 3
RETURNING *;

---------------------------- обновление читателя ----------------------------
UPDATE shelf.readers
SET
    surname = 'Петров',
    name = 'Алексей',
    second_name = 'Сергеевич',
    aboniment = 4568254,
    active_aboniment = True,
    birth_date = '1990-05-12',
    phone_number = '+79876543210',
    email = 'ivanov.alex@mail.ru',
    address = 'Казань, ул. Баумана, д. 3'
WHERE reader_id = 1
RETURNING *;

---------------------------- обновление работника ----------------------------
UPDATE shelf.workers
SET
    surname = 'Иванов',
    name = 'Иван',
    second_name = 'Иванович',
    role = 2,
    status = 1,
    birth_date = '1990-12-01',
    phone_number = '+77705874212',
    email = 'gfddgg@mai.com',
    address = 'Алматы, дом 10'
WHERE worker_id = 1
RETURNING *;

---------------------------- удаление книги ----------------------------
delete from book 
where book_id = 5
returning *;

```