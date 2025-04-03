from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from query import GET_BOOKS_QUERY, GET_BOOK_ID_QUERY, GET_READERS_QUERY, GET_WORKERS_QUERY, GET_WRITERS_QUERY # Проверь, что файлы существуют
from models import Book, Worker, History, Nation  # Проверь, что модели существуют
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

# Авторизация
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
        filters.append("w.last_name || '_' || w.name || '_' || w.second_name = :writer")
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
        filters.append("CONCAT(r.surname, ' ', r.name, ' ', r.second_name) ILIKE :reader")
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
        filters.append("CONCAT(w.surname, '_', w.name, '_', w.second_name) ILIKE :reader")
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
# Получение писателей библиотеки по параметрам запроса
@app.route('/writers', methods=['GET'])
@jwt_required()
def get_writers():
    writer_id = request.args.get("writer_id")
    writer_name = request.args.get("writer_name")
    nation = request.args.get("nation")
    book = request.args.get("book")

    query = GET_WRITERS_QUERY  # Базовый SQL-запрос
    params = {}
    filters = []

    if writer_name:
        filters.append("w.surname || ' ' || w.name || ' ' || w.second_name ILIKE :writer_name")
        params["writer_name"] = f"%{writer_name}%"

    if writer_id:
        filters.append("w.writer_id = :writer_id")
        params["writer_id"] = writer_id

    if nation:
        filters.append("n.country = :nation")
        params["nation"] = nation

    if book:
        filters.append('"Книги" ILIKE :book')  # Фильтр по уже агрегированному столбцу
        params["book"] = f"%{book}%"

    # Добавляем условия фильтрации
    if filters:
        query += " WHERE " + " AND ".join(filters)

    result = db.session.execute(text(query), params)
    rows = result.fetchall()
    column_names = result.keys()

    # Преобразуем строки в список словарей
    writers = [dict(zip(column_names, row)) for row in rows]

    return jsonify(writers)


if __name__ == '__main__':
    app.run(debug=True)
