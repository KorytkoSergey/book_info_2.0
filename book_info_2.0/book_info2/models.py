from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "book"
    __table_args__ = {"schema": "shelf"}  # Указываем схему shelf

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(255), nullable=False)
    date_publish = db.Column(db.Integer, nullable=False)

    language = db.Column(db.Integer, db.ForeignKey("shelf.lang.lang_id", ondelete="SET NULL"))
    publish = db.Column(db.Integer, db.ForeignKey("shelf.publish.publish_id", ondelete="SET NULL"))
    writer = db.Column(db.Integer, db.ForeignKey("shelf.writers.writer_id", ondelete="SET NULL"))
    genre = db.Column(db.Integer, db.ForeignKey("shelf.genre.genre_id", ondelete="SET NULL"))

    def __repr__(self):
        return f"<Book {self.book_name}, Published: {self.date_publish}>"

class Worker(db.Model):
    __tablename__ = "workers"
    __table_args__ = {"schema": "shelf"}

    worker_id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    second_name = db.Column(db.String(255))
    role = db.Column(db.Integer, db.ForeignKey("shelf.roles.role_id"), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey("shelf.status_worker.status_id"), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(255), unique=True)
    address = db.Column(db.Text)

    def __repr__(self):
        return f"<Worker {self.surname} {self.name}>"

class History(db.Model):
    __tablename__ = "history"
    __table_args__ = {"schema": "shelf"}

    history_id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey("shelf.readers.reader_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("shelf.book.book_id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("shelf.workers.worker_id"), nullable=False)
    borrow_date = db.Column(db.DateTime, default=db.func.now())
    return_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<History {self.history_id}: Reader {self.reader_id}, Book {self.book_id}>"

class Nation(db.Model):
    __tablename__ = "nation"
    __table_args__ = {"schema": "shelf"}

    nation_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Nation {self.country}>"

class Language(db.Model):
    __tablename__ = "lang"
    __table_args__ = {"schema": "shelf"}

    lang_id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Language {self.language}>"

class Genre(db.Model):
    __tablename__ = "genre"
    __table_args__ = {"schema": "shelf"}

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

class Publish(db.Model):
    __tablename__ = "publish"
    __table_args__ = {"schema": "shelf"}

    publish_id = db.Column(db.Integer, primary_key=True)
    publish_name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.Integer, db.ForeignKey("shelf.nation.nation_id"), nullable=True)

    def __repr__(self):
        return f"<Publish {self.publish_name}>"