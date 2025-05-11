from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from query import GET_BOOKS_QUERY, GET_BOOK_ID_QUERY, GET_READERS_QUERY, GET_WORKERS_QUERY, GET_WRITERS_QUERY
from query import POST_WRITERS_QUERY, POST_BOOKS_QUERY, POST_READERS_QUERY
from query import PUT_WRITERS_QUERY, PUT_READERS_QUERY, PUT_WORKERS_QUERY, PUT_BOOKS_QUERY 
from query import DELETE_BOOKS_QUERY
from models import Book, Worker, History, Nation  
from sqlalchemy.sql import text


app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/book_info_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Фиктивные пользователи
users = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "5678", "role": "user"},
}

############################ Авторизация ############################
## Регистрация нового пользователя (для примера)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        # identity теперь строка, а доп. данные (роль) передаем через additional_claims
        access_token = create_access_token(identity=username, additional_claims={"role": users[username]["role"]})
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

# Только для админов
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()  # Получаем имя пользователя
    claims = get_jwt()  # Получаем дополнительные данные из токена (например, роль)

    if claims.get("role") != "admin":
        return jsonify({"msg": "Access denied"}), 403
    return jsonify({"msg": f"Welcome, {current_user}!"})

# Только для пользователей
@app.route('/user', methods=['GET'])
@jwt_required()
def user_only():
    current_user = get_jwt_identity()  # Получаем имя пользователя
    claims = get_jwt()  # Получаем дополнительные данные из токена (например, роль)

    if claims.get("role") != "user":
        return jsonify({"msg": "Access denied"}), 403
    return jsonify({"msg": f"Welcome, {current_user}!"})

############################ GET - запросы ############################

# Получение книг по параметрам запроса
@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    writer = request.args.get("writer")
    year = request.args.get("year")
    language = request.args.get("language")
    book_name = request.args.get("book_name")
    genre = request.args.get("genre")
    publish = request.args.get("publish")
    place = request.args.get("place", None)  # Значение по умолчанию None

    query = GET_BOOKS_QUERY  # Используем SQL-запрос из `queries.py`
    params = {}

    filters = []

    if writer:
        filters.append("CONCAT(w.last_name, '_', w.name, '_', w.second_name) ILIKE :writer")
        params["writer"] = writer
    if year:
        filters.append("b.date_publish = :year")
        params["year"] = year
    if language:
        filters.append("l.language = :language")
        params["language"] = language
    if book_name:
        filters.append("b.book_name = :book_name")
        params["book_name"] = book_name
    if genre:
        filters.append("g.genre_name = :genre")
        params["genre"] = genre
    if publish:
        filters.append("p.publish_name = :publish")
        params["publish"] = publish

    if place:
        if place == "on_hands":
            filters.append("h.return_date IS NULL")
        elif place == "in_library":
            filters.append("h.return_date IS NOT NULL")

    # Добавляем условия корректно
    if filters:
        query += " AND " + " AND ".join(filters)  # Исправлено, теперь без второго WHERE

    result = db.session.execute(text(query), params)
    books = [dict(zip(result.keys(), row)) for row in result]

    return jsonify(books)

# Получение книги по id
@app.route('/books/<int:num>', methods=['GET'])
def get_book_id(num):
    result = db.session.execute(GET_BOOK_ID_QUERY, {"num": num})
    rows = [dict(row) for row in result.mappings().all()]  # Преобразуем RowMapping в словари

    if not rows:
        return jsonify({"error": "Книга не найдена"}), 404  

    return jsonify(rows)

# Получение читателей по параметрам запроса
@app.route('/readers', methods=['GET'])
@jwt_required()
def get_readers():
    reader = request.args.get("reader")
    aboniment = request.args.get("aboniment")
    is_active = request.args.get("is_active")
    birth_date_from = request.args.get("birth_date_from")
    birth_date_to = request.args.get("birth_date_to")
    phone_number = request.args.get("phone_number")
    email = request.args.get("email")
    min_books = request.args.get("min_books")
    max_books = request.args.get("max_books")

    query = GET_READERS_QUERY  # Используем базовый SQL-запрос
    params = {}
    filters = []

    if reader:
        filters.append("CONCAT(r.surname, '_', r.name, '_', r.second_name) ILIKE :reader")
        params["reader"] = f"%{reader}%"

    if aboniment:
        filters.append("r.aboniment = :aboniment")
        params["aboniment"] = aboniment

    if is_active:
        filters.append("r.active_aboniment = :is_active")
        params["is_active"] = is_active

    if birth_date_from:
        filters.append("r.birth_date >= :birth_date_from")
        params["birth_date_from"] = birth_date_from

    if birth_date_to:
        filters.append("r.birth_date <= :birth_date_to")
        params["birth_date_to"] = birth_date_to

    if phone_number:
        filters.append("r.phone_number ILIKE :phone_number")
        params["phone_number"] = f"%{phone_number}%"

    if email:
        filters.append("r.email ILIKE :email")
        params["email"] = f"%{email}%"

    if min_books:
        filters.append("""
            (SELECT COUNT(*) FROM shelf.history h 
             WHERE h.reader_id = r.reader_id AND h.return_date IS NULL) >= :min_books
        """)
        params["min_books"] = min_books

    if max_books:
        filters.append("""
            (SELECT COUNT(*) FROM shelf.history h 
             WHERE h.reader_id = r.reader_id AND h.return_date IS NULL) <= :max_books
        """)
        params["max_books"] = max_books

    # Добавляем условия фильтрации
    if filters:
        query += " WHERE " + " AND ".join(filters)

    result = db.session.execute(text(query), params)
    rows = result.fetchall()  # Получаем список кортежей
    column_names = result.keys()  # Получаем названия колонок

    # Преобразуем строки в список словарей
    readers = [dict(zip(column_names, row)) for row in rows]

    return jsonify(readers)


# Получение работников библиотеки по параметрам запроса
@app.route('/workers', methods=['GET'])
@jwt_required()
def get_workers():
    worker_id = request.args.get("worker_id")
    worker_name = request.args.get("worker_name")
    role = request.args.get("role")
    status = request.args.get("status")

    query = GET_WORKERS_QUERY  # Используем базовый SQL-запрос
    params = {}
    filters = []

    if worker_name:
        filters.append("CONCAT(w.surname, '_', w.name, '_', w.second_name) ILIKE :worker_name")
        params["worker_name"] = f"%{worker_name}%"

    if worker_id:
        filters.append("w.worker_id = :worker_id")
        params["worker_id"] = worker_id

    if role:
        filters.append("r.role = :role")
        params["role"] = role

    if status:
        filters.append("s.status = :status")
        params["status"] = status


    # Добавляем условия фильтрации
    if filters:
        query += " WHERE " + " AND ".join(filters)

    result = db.session.execute(text(query), params)
    rows = result.fetchall()  # Получаем список кортежей
    column_names = result.keys()  # Получаем названия колонок

    # Преобразуем строки в список словарей
    workers = [dict(zip(column_names, row)) for row in rows]

    return jsonify(workers)


# Получение писателей библиотеки по параметрам запроса
@app.route('/writers', methods=['GET'])
@jwt_required()
def get_writers():
    writer_id = request.args.get("writer_id")
    writer_name = request.args.get("writer_name")
    nation = request.args.get("nation")
    book = request.args.get("book")
    only_without_books = request.args.get("only_without_books")

    query = GET_WRITERS_QUERY  # Базовый SQL-запрос без WHERE
    params = {}
    filters = []

    # Поиск по ФИО (FIO — псевдоним в CTE)
    if writer_name:
        filters.append('FIO ILIKE :writer_name')
        params["writer_name"] = f"%{writer_name}%"

    # Поиск по writer_id
    if writer_id:
        filters.append('writer_id = :writer_id')
        params["writer_id"] = writer_id

    # Поиск по нации
    if nation:
        filters.append('country = :nation')
        params["nation"] = nation

    # Поиск по названию книги
    if book:
        filters.append('books_name ILIKE :book')
        params["book"] = f"%{book}%"

    # Фильтр: только авторы без книг
    if only_without_books == 'true':
        filters.append("books_name = 'Нет книг'")

    # Добавляем фильтры в запрос
    if filters:
        query += " WHERE " + " AND ".join(filters)

    result = db.session.execute(text(query), params)
    rows = result.fetchall()
    column_names = result.keys()

    # Преобразуем строки в список словарей
    writers = [dict(zip(column_names, row)) for row in rows]

    return jsonify(writers)

############################ POST - запросы ############################
# Добавление нового писателя
@app.route('/writers', methods=['POST'])
@jwt_required()
def add_writer():
    data = request.get_json()

    last_name = data.get('last_name')
    name = data.get('name')
    second_name = data.get('second_name')
    birth_date = data.get('birth_date')
    nationality = data.get('nationality')  # ID нации
    info = data.get('info', '')

    insert_query = POST_WRITERS_QUERY  # должен содержать RETURNING *

    try:
        result = db.session.execute(
            text(insert_query),
            {
                "last_name": last_name,
                "name": name,
                "second_name": second_name,
                "birth_date": birth_date,
                "nationality": nationality,
                "info": info,
            }
        )
        db.session.commit()

        new_writer_row = result.fetchone()
        column_names = result.keys()
        new_writer = dict(zip(column_names, new_writer_row))

        return jsonify({"message": "Писатель добавлен", "writer_info": new_writer}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Добавление новой книги
@app.route('/books', methods=['POST'])
@jwt_required()
def add_books():
    data = request.get_json()

    book_name = data.get('book_name')
    date_publish = data.get('date_publish')
    language = data.get('language')
    publish = data.get('publish')
    writer = data.get('writer')  # ID нации
    genre = data.get('genre')

    insert_query = POST_BOOKS_QUERY  # должен содержать RETURNING *

    try:
        result = db.session.execute(
            text(insert_query),
            {
                "book_name": book_name,
                "date_publish": date_publish,
                "language": language,
                "publish": publish,
                "writer": writer,
                "genre": genre,
            }
        )
        db.session.commit()

        new_book_row = result.fetchone()
        book_names = result.keys()
        new_book = dict(zip(book_names, new_book_row))

        return jsonify({"message": "Книга добавлена", "book_info": new_book}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Добавление нового читателя
@app.route('/readers', methods=['POST'])
@jwt_required()
def add_readers():
    data = request.get_json()

    surname = data.get('surname')
    name = data.get('name')
    second_name = data.get('second_name')
    aboniment = data.get('aboniment')
    active_aboniment = data.get('active_aboniment')
    birth_date = data.get('birth_date')
    phone_number = data.get('phone_number')
    email = data.get('email')
    address = data.get('address')

    insert_query = POST_READERS_QUERY  # должен содержать RETURNING *

    try:
        result = db.session.execute(
            text(insert_query),
            {
                "surname": surname,
                "name": name,
                "second_name": second_name,
                "aboniment": aboniment,
                "active_aboniment": active_aboniment,
                "birth_date": birth_date,
                "phone_number": phone_number,
                "email": email,
                "address": address,
            }
        )
        db.session.commit()

        new_reader_row = result.fetchone()
        reader_names = result.keys()
        new_reader = dict(zip(reader_names, new_reader_row))

        return jsonify({"message": "Читатель добавлен", "reader_info": new_reader}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

############################ PUT - запросы ############################
# Изменение читателя
@app.route('/readers/<int:reader_id>', methods=['PUT'])
@jwt_required()
def update_reader(reader_id):
    data = request.get_json()

    try:
        update_query = PUT_READERS_QUERY

        result = db.session.execute(
            text(update_query),
            {
                "reader_id": reader_id,
                "surname": data.get("surname"),
                "name": data.get("name"),
                "second_name": data.get("second_name"),
                "aboniment": data.get("aboniment"),
                "active_aboniment": data.get("active_aboniment"),
                "birth_date": data.get("birth_date"),
                "phone_number": data.get("phone_number"),
                "email": data.get("email"),
                "address": data.get("address")
            }
        )

        db.session.commit()
        updated_reader = result.fetchone()

        if updated_reader is None:
            return jsonify({"error": "Читатель не найден"}), 404

        return jsonify({
            "message": "Читатель успешно обновлён",
            "reader": dict(updated_reader._mapping)
            }), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Изменение писателя
@app.route('/writers/<int:writer_id>', methods=['PUT'])
@jwt_required()
def update_writer(writer_id):
    data = request.get_json()

    try:
        update_query = PUT_WRITERS_QUERY

        result = db.session.execute(
            text(update_query),
            {
                "writer_id": writer_id,
                "last_name": data.get("last_name"),
                "name": data.get("name"),
                "second_name": data.get("second_name"),
                "birth_date": data.get("birth_date"),
                "nationality": data.get("nationality"),
                "info": data.get("info")
            }
        )

        db.session.commit()
        updated_writer = result.fetchone()

        if updated_writer is None:
            return jsonify({"error": "Писатель не найден"}), 404

        return jsonify({
            "message": "Писатель успешно обновлён",
            "writer": dict(updated_writer._mapping)
            }), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Изменение работника
@app.route('/workers/<int:worker_id>', methods=['PUT'])
@jwt_required()
def update_worker(worker_id):
    data = request.get_json()

    try:
        update_query = PUT_WORKERS_QUERY

        result = db.session.execute(
            text(update_query),
            {
                "worker_id": worker_id,
                "surname": data.get("surname"),
                "name": data.get("name"),
                "second_name": data.get("second_name"),
                "role": data.get("role"),
                "status": data.get("status"),
                "birth_date": data.get("birth_date"),
                "phone_number": data.get("phone_number"),
                "email": data.get("email"),
                "address": data.get("address")
            }
        )

        db.session.commit()
        updated_worker = result.fetchone()

        if updated_worker is None:
            return jsonify({"error": "Работник не найден"}), 404

        return jsonify({
            "message": "Работник успешно обновлён",
            "worker": dict(updated_worker._mapping)
            }), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Изменение книги
@app.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()

    try:
        update_query = PUT_BOOKS_QUERY

        result = db.session.execute(
            text(update_query),
            {
                "book_id": book_id,
                "book_name": data.get("book_name"),
                "date_publish": data.get("date_publish"),
                "language": data.get("language"),
                "publish": data.get("publish"),
                "writer": data.get("writer"),
                "genre": data.get("genre")
            }
        )

        db.session.commit()
        updated_book = result.fetchone()

        if updated_book is None:
            return jsonify({"error": "Книга не найдена"}), 404

        return jsonify({
            "message": "Книга успешно обновлена",
            "book": dict(updated_book._mapping)
            }), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

############################ DELETE - запросы ############################
# Удаление книги
@app.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    try:
        result = db.session.execute(
            text(DELETE_BOOKS_QUERY),
            {"book_id": book_id}
        )
        db.session.commit()

        if result.rowcount == 0:
            return jsonify({"error": "Книга не найдена"}), 404

        return jsonify({"message": "Книга успешно удалена"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
