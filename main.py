"""Импортированные модули"""
from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
import uvicorn

app = FastAPI()


def get_db_connection():
    """Подключение к БД"""
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=412-04\\MSSQLSERVER2024;"
            "DATABASE=LibraryDB;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка БД: {str(e)}") from e


# Модели данных
class Author(BaseModel):
    """Класс автор"""
    name: str
    bio: Optional[str] = None


class Genre(BaseModel):
    """Класс жанр"""
    name: str
    description: Optional[str] = None


class Book(BaseModel):
    """Класс книга"""
    title: str
    author_id: int
    genre_id: int
    isbn: str
    publication_year: int
    available_copies: int


class Reader(BaseModel):
    """Класс читатель"""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None


class BookLoan(BaseModel):
    """Класс для того, чтобы взять книгу"""
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date


def execute_query(query, params=None, fetch=False):
    """Функция для выполнения запросов"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            result = cursor.fetchone()[0]
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


@app.on_event("startup")
def startup():
    """Проверка подключения к бд"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        print(f"Подключено к SQL Server: {cursor.fetchone()[0]}")
        conn.close()
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка запуска: {str(e)}") from e


@app.post("/authors/")
def create_author(author: Author):
    """Создание автора"""
    try:
        author_id = execute_query(
            "INSERT INTO Authors (name, bio) VALUES (?, ?)",
            (author.name, author.bio))
        return {"author_id": author_id, "message": "Автор создан"}
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


@app.get("/authors/")
def get_authors():
    """Получить авторов"""
    try:
        rows = execute_query(
            "SELECT author_id, name, bio FROM Authors", fetch=True)
        return [{"author_id": r[0], "name": r[1], "bio": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {str(e)}") from e


@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    """Удалить автора по ID """
    try:
        books = execute_query(
            "SELECT COUNT(*) FROM Books WHERE author_id = ?",
            (author_id,), fetch=True)
        if books[0][0] > 0:
            raise HTTPException(400, "Нельзя удалить автора с книгами")
        execute_query("DELETE FROM Authors WHERE author_id = ?", (author_id,))
        return {"message": "Автор удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка удаления: {str(e)}") from e


@app.post("/genres/")
def create_genre(genre: Genre):
    """Создать жанр"""
    try:
        genre_id = execute_query(
            "INSERT INTO Genres (name, description) VALUES (?, ?)", 
            (genre.name, genre.description))
        return {"genre_id": genre_id, "message": "Жанр создан"}
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


@app.get("/genres/")
def get_genres():
    """Получить жанры"""
    try:
        rows = execute_query(
            "SELECT genre_id, name, description FROM Genres", fetch=True)
        return [
            {"genre_id": r[0], "name": r[1],
                "description": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {str(e)}") from e


# Книги
@app.post("/books/")
def create_book(book: Book):
    """Создать книгу"""
    try: 
        book_id = execute_query(
            "INSERT INTO Books (title, author_id, genre_id, isbn,publication_year, available_copies) VALUES (?, ?, ?, ?, ?, ?)",
            (book.title, book.author_id, 
                book.genre_id, book.isbn, book.publication_year,
                book.available_copies)
            )
        return {"book_id": book_id, "message": "Книга создана"}
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


@app.get("/books/")
def get_books():
    """Получить книгу"""
    try:
        rows = execute_query(
            "SELECT book_id, title, author_id, genre_id, isbn, publication_year, available_copies FROM Books",
            fetch=True)
        return [
            {"book_id": r[0], "title": r[1], "author_id": r[2], "genre_id": r[3], ""
             "isbn": r[4], "publication_year": r[5],
             "available_copies": r[6]} for r in rows]
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {str(e)}") from e



@app.post("/readers/")
def create_reader(reader: Reader):
    """создание читателя"""
    try:
        reader_id = execute_query(
            "INSERT INTO Readers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
            (reader.first_name, reader.last_name, reader.email, reader.phone)
        )
        return {"reader_id": reader_id, "message": "Читатель создан"}
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


@app.get("/readers/")
def get_readers():
    """Получить читателей"""
    try:
        rows = execute_query(
            "SELECT reader_id, first_name, last_name, email, phone FROM Readers",
            fetch=True)
        return [{"reader_id": r[0],
                 "first_name": r[1],
                 "last_name": r[2],
                 "email": r[3],
                 "phone": r[4]} for r in rows]
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {str(e)}") from e


@app.post("/book-loans/")
def create_book_loan(loan: BookLoan):
    """Создание записи о выдаче книги"""
    try:
        available = execute_query(
            "SELECT available_copies FROM Books WHERE book_id = ?",
            (loan.book_id,), fetch=True)
        if not available or available[0][0] <= 0:
            raise HTTPException(400, "Книга недоступна")
        loan_id = execute_query(
            "INSERT INTO BookLoans (book_id, reader_id, loan_date, due_date) VALUES (?, ?, ?, ?)",
            (loan.book_id, loan.reader_id, loan.loan_date, loan.due_date)
        )
        execute_query(
            "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?",
            (loan.book_id,))  
        return {"loan_id": loan_id, "message": "Книга выдана"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


@app.get("/book-loans/")
def get_book_loans():
    """Получение записей о выдаче книг"""
    try:
        rows = execute_query("SELECT loan_id, book_id, reader_id, loan_date, due_date, return_date FROM BookLoans", fetch=True)
        return [{"loan_id": r[0], "book_id": r[1], "reader_id": r[2], "loan_date": r[3], "due_date": r[4], "return_date": r[5]} for r in rows]
    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка: {str(e)}") from e


@app.put("/book-loans/{loan_id}/return")
def return_book(loan_id: int):
    """Возвращение книги"""
    try:
        loan = execute_query(
            "SELECT book_id FROM BookLoans WHERE loan_id = ? AND return_date IS NULL",
            (loan_id,), fetch=True)
        if not loan:
            raise HTTPException(404, "Выдача не найдена")
        execute_query(
            "UPDATE BookLoans SET return_date = ? WHERE loan_id = ?",
            (date.today(), loan_id))
        execute_query(
            "UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = ?",
            (loan[0][0],))
        return {"message": "Книга возвращена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка: {str(e)}") from e


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000, reload=True)