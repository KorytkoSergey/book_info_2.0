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
SELECT
    w.writer_id,
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Писателя",
    w.birth_date,
    n.country,
    COALESCE(  
        (SELECT STRING_AGG(b.book_name, ', ')  
         FROM shelf.book b  
         WHERE b.writer = w.writer_id
        ), 'Нет книг'
    ) AS "Книги",
    w.info
FROM shelf.writers w
JOIN shelf.nation n ON w.nationality = n.nation_id

;
--- писатели без книг
SELECT
    w.writer_id,
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Писателя",
    w.birth_date,
    n.country,
    COALESCE(
        (SELECT STRING_AGG(b.book_name, ', ')
         FROM shelf.book b
         WHERE b.writer = w.writer_id
        ), 'Нет книг'
    ) AS "Книги",
    w.info
FROM shelf.writers w
JOIN shelf.nation n ON w.nationality = n.nation_id
GROUP BY w.writer_id, w.last_name, w.name, w.second_name, w.birth_date, n.country, w.info
HAVING COALESCE(
        (SELECT STRING_AGG(b.book_name, ', ')
         FROM shelf.book b
         WHERE b.writer = w.writer_id
        ), 'Нет книг'
    ) <> 'Нет книг';


SELECT
    w.writer_id,
    w.last_name || ' ' || w.name || ' ' || w.second_name AS "ФИО Писателя",
    w.birth_date,
    n.country,
    q.books_name,
    w.info
FROM shelf.writers w
JOIN shelf.nation n ON w.nationality = n.nation_id
left join (    -------вместо case сделать with
SELECT q.writer,
	case 
		when STRING_AGG(q.book_name, ', ') = 'Колобок' then 'Нет книг'
		else STRING_AGG(q.book_name, ', ')
	end as books_name
         FROM shelf.book q
         group by q.writer
) q on q.writer = w.writer_id;



