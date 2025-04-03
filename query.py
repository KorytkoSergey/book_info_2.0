from sqlalchemy.sql import text

GET_BOOKS_QUERY = """
    SELECT 
        b.book_name AS "Название",
        b.date_publish AS "Дата издания",
        l.language AS "Язык",
        p.publish_name AS "Издательство",
        w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Автора",
        g.genre_name AS "Жанр",
        COALESCE(  
            (SELECT STRING_AGG(r.surname || ' ' || r.name || ' ' || r.second_name, ', ') 
             FROM shelf.history h
             JOIN shelf.readers r ON h.reader_id = r.reader_id
             WHERE h.book_id = b.book_id
            ), 'Нет читателей'
        ) AS "Читатели",
        COALESCE(  
            (SELECT STRING_AGG(w.surname || ' ' || w.name || ' ' || w.second_name, ', ') 
             FROM shelf.history h
             JOIN shelf.workers w ON h.worker_id = w.worker_id
             WHERE h.book_id = b.book_id
            ), 'Ни кем не выдавалась'
        ) AS "Работник библиотеки",
        CASE 
            WHEN h.return_date IS NULL THEN 'На руках'
            ELSE 'В библиотеке'
        END AS "Нахождение"
    FROM shelf.book b
    JOIN shelf.lang l ON b.language = l.lang_id
    JOIN shelf.publish p ON b.publish = p.publish_id
    JOIN shelf.writers w ON b.writer = w.writer_id
    JOIN shelf.genre g ON b.genre = g.genre_id
    LEFT JOIN shelf.history h ON b.book_id = h.book_id
    WHERE 1=1
"""

GET_BOOK_ID_QUERY = text("""
SELECT  
    b.book_name AS "Название",
    b.date_publish AS "Дата издания",
    l.language AS "Язык",
    p.publish_name AS "Издательство",
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Автора",
    g.genre_name AS "Жанр",
    COALESCE(
        STRING_AGG(DISTINCT r.surname || ' ' || r.name || ' ' || r.second_name, ', '), 
        'Нет читателей'
    ) AS "Читатели",
    COALESCE(
        STRING_AGG(DISTINCT w2.surname || ' ' || w2.name || ' ' || w2.second_name, ', '), 
        'Ни кем не выдавалась'
    ) AS "Работник библиотеки",
    CASE 
        WHEN COUNT(h.return_date) FILTER (WHERE h.return_date IS NULL) > 0 
        THEN 'На руках'
        ELSE 'В библиотеке'
    END AS "Нахождение"
FROM shelf.book b
JOIN shelf.lang l ON b.language = l.lang_id
JOIN shelf.publish p ON b.publish = p.publish_id
JOIN shelf.writers w ON b.writer = w.writer_id
JOIN shelf.genre g ON b.genre = g.genre_id
LEFT JOIN shelf.history h ON b.book_id = h.book_id
LEFT JOIN shelf.readers r ON h.reader_id = r.reader_id
LEFT JOIN shelf.workers w2 ON h.worker_id = w2.worker_id
WHERE b.book_id = :num  
GROUP BY b.book_id, b.book_name, b.date_publish, l.language, p.publish_name, 
         w.last_name, w.name, w.second_name, g.genre_name;
""")

GET_READERS_QUERY = """
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
         WHERE h.reader_id = r.reader_id AND h.return_date IS NULL
        ), 'Не брал книг'
    ) AS "Книги на руках"
FROM shelf.readers r
"""
GET_WORKERS_QUERY = """
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
join shelf.status_worker s on w.status = s.status_id
"""

GET_WRITERS_QUERY = """
SELECT
    w.writer_id,
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Писателя",
    w.birth_date,
    n.country,
    q.books_name,
    w.info
FROM shelf.writers w
JOIN shelf.nation n ON w.nationality = n.nation_id
left join (
SELECT q.writer,
STRING_AGG(q.book_name, ', ') as books_name
         FROM shelf.book q
         group by q.writer
) q on q.writer = w.writer_id;
"""