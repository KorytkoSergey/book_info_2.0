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
SELECT * FROM writers_result
"""

POST_WRITERS_QUERY = """
        INSERT INTO shelf.writers (last_name, name, second_name, birth_date, nationality, info)
        VALUES (:last_name, :name, :second_name, :birth_date, :nationality, :info)
        RETURNING *;
    """

POST_BOOKS_QUERY = """
        INSERT INTO shelf.book (book_name, date_publish, language, publish, writer, genre)
        VALUES (:book_name, :date_publish, :language, :publish, :writer, :genre)
        returning *;
    """

POST_READERS_QUERY = """
        INSERT INTO shelf.readers (surname, name, second_name, aboniment, active_aboniment, birth_date, phone_number, email, address)
        VALUES (:surname, :name, :second_name, :aboniment, :active_aboniment, :birth_date, :phone_number, :email, :address)
        returning *;
    """

PUT_READERS_QUERY = """
    UPDATE shelf.readers
    SET
        surname = :surname,
        name = :name,
        second_name = :second_name,
        aboniment = :aboniment,
        active_aboniment = :active_aboniment,
        birth_date = :birth_date,
        phone_number = :phone_number,
        email = :email,
        address = :address
    WHERE reader_id = :reader_id
    RETURNING *;
"""


PUT_WRITERS_QUERY = """
    UPDATE shelf.writers
    SET
        last_name = :last_name,
        name = :name,
        second_name = :second_name,
        birth_date = :birth_date,
        nationality = :nationality,
        info = :info
    WHERE writer_id = :writer_id
    RETURNING *;
    """

PUT_WORKERS_QUERY = """
    UPDATE shelf.workers
    SET
        surname = :surname,
        name = :name,
        second_name = :name,
        role = :role,
        status = :status,
        birth_date = :birth_date,
        phone_number = :phone_number,
        email = :email,
        address = :address
    WHERE worker_id = :worker_id
    RETURNING *;
    """

PUT_BOOKS_QUERY = """
    UPDATE shelf.book
    SET
        book_name = :book_name,
        date_publish = :date_publish,
        language = :language,
        publish = :publish,
        writer = :writer,
        genre = :genre
    WHERE book_id = :book_id
    RETURNING *; 
"""

DELETE_BOOKS_QUERY = """
    DELETE FROM shelf.book
    WHERE book_id = :book_id
    RETURNING *;
"""