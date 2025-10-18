from fastapi import FastAPI
import sqlite3
from datetime import date

app = FastAPI()

# Создаем базу данных и таблицы
conn = sqlite3.connect("simple_library.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bio TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Genres (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER,
        genre_id INTEGER,
        isbn TEXT UNIQUE,
        publication_year INTEGER,
        available_copies INTEGER DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Readers (
        reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS BookLoans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        reader_id INTEGER,
        loan_date DATE NOT NULL,
        due_date DATE NOT NULL,
        return_date DATE
    )
''')

conn.commit()
conn.close()

# Авторы
@app.post("/authors/")
def create_author(name: str, bio: str = ""):
    """Создание автора"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Authors (name, bio) VALUES (?, ?)", (name, bio))
        conn.commit()
        author_id = cursor.lastrowid
        return {"author_id": author_id, "message": "Автор создан"}
    except:
        return {"error": "Такой автор уже существует"}
    finally:
        conn.close()

@app.get("/authors/")
def get_authors():
    """Получить всех авторов"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author_id, name, bio FROM Authors")
    authors = cursor.fetchall()
    conn.close()
    
    if not authors:
        return {"error": "Список авторов пуст"}
    
    return [{"author_id": a[0], "name": a[1], "bio": a[2]} for a in authors]

@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    """Удаление автора"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        # Проверяем, есть ли книги у этого автора
        cursor.execute("SELECT COUNT(*) FROM Books WHERE author_id = ?", (author_id,))
        book_count = cursor.fetchone()[0]
        
        if book_count > 0:
            return {"error": "Нельзя удалить автора, у которого есть книги"}
        
        # Удаляем автора
        cursor.execute("DELETE FROM Authors WHERE author_id = ?", (author_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return {"error": "Автор не найден"}
        
        return {"message": "Автор удален"}
    except Exception as e:
        return {"error": f"Ошибка при удалении автора: {str(e)}"}
    finally:
        conn.close()

# Жанры
@app.post("/genres/")
def create_genre(name: str, description: str = ""):
    """Создание жанра"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Genres (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        genre_id = cursor.lastrowid
        return {"genre_id": genre_id, "message": "Жанр создан"}
    except:
        return {"error": "Такой жанр уже существует"}
    finally:
        conn.close()

@app.get("/genres/")
def get_genres():
    """Получить все жанры"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT genre_id, name, description FROM Genres")
    genres = cursor.fetchall()
    conn.close()
    
    if not genres:
        return {"error": "Список жанров пуст"}
    
    return [{"genre_id": g[0], "name": g[1], "description": g[2]} for g in genres]

# Книги
@app.post("/books/")
def create_book(title: str, author_id: int, genre_id: int, isbn: str, publication_year: int, available_copies: int = 1):
    """Создание книги"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Books (title, author_id, genre_id, isbn, publication_year, available_copies) VALUES (?, ?, ?, ?, ?, ?)",
            (title, author_id, genre_id, isbn, publication_year, available_copies)
        )
        conn.commit()
        book_id = cursor.lastrowid
        return {"book_id": book_id, "message": "Книга создана"}
    except:
        return {"error": "Такая книга уже существует"}
    finally:
        conn.close()

@app.get("/books/")
def get_books():
    """Получить все книги"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author_id, genre_id, isbn, publication_year, available_copies FROM Books")
    books = cursor.fetchall()
    conn.close()
    
    if not books:
        return {"error": "Список книг пуст"}
    
    return [{"book_id": b[0], "title": b[1], "author_id": b[2], "genre_id": b[3], "isbn": b[4], "publication_year": b[5], "available_copies": b[6]} for b in books]

# Читатели
@app.post("/readers/")
def create_reader(first_name: str, last_name: str, email: str, phone: str = ""):
    """Создание читателя"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Readers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, phone)
        )
        conn.commit()
        reader_id = cursor.lastrowid
        return {"reader_id": reader_id, "message": "Читатель создан"}
    except:
        return {"error": "Такой читатель уже существует"}
    finally:
        conn.close()

@app.get("/readers/")
def get_readers():
    """Получить всех читателей"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT reader_id, first_name, last_name, email, phone FROM Readers")
    readers = cursor.fetchall()
    conn.close()
    
    if not readers:
        return {"error": "Список читателей пуст"}
    
    return [{"reader_id": r[0], "first_name": r[1], "last_name": r[2], "email": r[3], "phone": r[4]} for r in readers]

# Выдача книг
@app.post("/book-loans/")
def create_book_loan(book_id: int, reader_id: int, loan_date: str, due_date: str):
    """Создание записи о выдаче книги"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        # Проверяем доступность книги
        cursor.execute("SELECT available_copies FROM Books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        
        if not book or book[0] <= 0:
            return {"error": "Книга недоступна"}
        
        # Создаем запись о выдаче
        cursor.execute(
            "INSERT INTO BookLoans (book_id, reader_id, loan_date, due_date) VALUES (?, ?, ?, ?)",
            (book_id, reader_id, loan_date, due_date)
        )
        
        # Уменьшаем количество доступных копий
        cursor.execute("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?", (book_id,))
        
        conn.commit()
        loan_id = cursor.lastrowid
        return {"loan_id": loan_id, "message": "Книга выдана"}
    except:
        return {"error": "Ошибка выдачи книги"}
    finally:
        conn.close()

@app.get("/book-loans/")
def get_book_loans():
    """Получить все выдачи книг"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT loan_id, book_id, reader_id, loan_date, due_date, return_date FROM BookLoans")
    loans = cursor.fetchall()
    conn.close()
    
    if not loans:
        return {"error": "Список выдач книг пуст"}
    
    return [{"loan_id": l[0], "book_id": l[1], "reader_id": l[2], "loan_date": l[3], "due_date": l[4], "return_date": l[5]} for l in loans]

@app.put("/book-loans/{loan_id}/return")
def return_book(loan_id: int):
    """Возврат книги"""
    conn = sqlite3.connect("simple_library.db")
    cursor = conn.cursor()
    try:
        # Находим выдачу
        cursor.execute("SELECT book_id FROM BookLoans WHERE loan_id = ? AND return_date IS NULL", (loan_id,))
        loan = cursor.fetchone()
        
        if not loan:
            return {"error": "Выдача не найдена"}
        
        # Отмечаем возврат
        cursor.execute("UPDATE BookLoans SET return_date = ? WHERE loan_id = ?", (str(date.today()), loan_id))
        
        # Увеличиваем количество доступных копий
        cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = ?", (loan[0],))
        
        conn.commit()
        return {"message": "Книга возвращена"}
    except:
        return {"error": "Ошибка возврата книги"}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)