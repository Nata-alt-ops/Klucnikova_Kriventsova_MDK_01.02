import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"


def test_get_all_authors():
    """Получение всех авторов"""
    response = requests.get(f"{BASE_URL}/authors/")
    print("GET Authors Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_author(author_data):
    """Создание автора"""
    response = requests.post(f"{BASE_URL}/authors/", json=author_data)
    print("POST Author Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response.json().get('author_id')

def test_delete_author(author_id):
    """Удаление автора"""
    response = requests.delete(f"{BASE_URL}/authors/{author_id}")
    print("DELETE Author Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_all_genres():
    """Получение всех жанров"""
    response = requests.get(f"{BASE_URL}/genres/")
    print("GET Genres Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_genre(genre_data):
    """Создание жанра"""
    response = requests.post(f"{BASE_URL}/genres/", json=genre_data)
    print("POST Genre Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response.json().get('genre_id')

def test_get_all_books():
    """Получение всех книг"""
    response = requests.get(f"{BASE_URL}/books/")
    print("GET Books Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_book(book_data):
    """Создание книги"""
    response = requests.post(f"{BASE_URL}/books/", json=book_data)
    print("POST Book Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response.json().get('book_id')

def test_get_all_readers():
    """Получение всех читателей"""
    response = requests.get(f"{BASE_URL}/readers/")
    print("GET Readers Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_reader(reader_data):
    """Создание читателя"""
    response = requests.post(f"{BASE_URL}/readers/", json=reader_data)
    print("POST Reader Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response.json().get('reader_id')

def test_get_all_book_loans():
    """Получение всех выдач книг"""
    response = requests.get(f"{BASE_URL}/book-loans/")
    print("GET Book Loans Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_book_loan(loan_data):
    """Создание записи о выдаче книги"""
    response = requests.post(f"{BASE_URL}/book-loans/", json=loan_data)
    print("POST Book Loan Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response.json().get('loan_id')

def test_return_book(loan_id):
    """Возврат книги"""
    response = requests.put(f"{BASE_URL}/book-loans/{loan_id}/return")
    print("PUT Return Book Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def main():
    
    print("1. ТЕСТЫ АВТОРОВ")
    print("-" * 50)
    
  
    test_get_all_authors()
    
  
    test_author = {
        "name": "Тестовый Автор",
        "bio": "Биография тестового автора"
    }
    author_id = test_create_author(test_author)
    
  
    test_get_all_authors()
    
    print("\n2. ТЕСТЫ ЖАНРОВ")
    print("-" * 50)
    
 
    test_get_all_genres()
    
  
    test_genre = {
        "name": "Тестовый Жанр",
        "description": "Описание тестового жанра"
    }
    genre_id = test_create_genre(test_genre)
    
   
    test_get_all_genres()
    
    print("\n3. ТЕСТЫ КНИГ")
    print("-" * 50)
    
   
    test_get_all_books()
    
    # Создание тестовой книги
    test_book = {
        "title": "Тестовая Книга",
        "author_id": 1,
        "genre_id": 1,
        "isbn": "978-5-17-090138-2",
        "publication_year": 2024,
        "available_copies": 5
    }
    book_id = test_create_book(test_book)
    
   
    test_get_all_books()
    
    print("\n4. ТЕСТЫ ЧИТАТЕЛЕЙ")
    print("-" * 50)

    test_get_all_readers()
    
  
    test_reader = {
        "first_name": "Тест",
        "last_name": "Тестовый",
        "email": "vilka@mail.com",
        "phone": "+7-999-999-99-99"
    }
    reader_id = test_create_reader(test_reader)
    
    
    test_get_all_readers()
    
    print("\n5. ТЕСТЫ ВЫДАЧИ КНИГ")
    print("-" * 50)
    
    
    test_get_all_book_loans()
    
    
    today = date.today()
    due_date = today + timedelta(days=14)
    
    test_loan = {
        "book_id": 9,
        "reader_id": 9,
        "loan_date": str(today),
        "due_date": str(due_date)
    }
    loan_id = test_create_book_loan(test_loan)
    
   
    test_get_all_book_loans()
    
   
    test_return_book(loan_id)
    
    
    test_get_all_book_loans()
    
    print("\n6. ТЕСТЫ УДАЛЕНИЯ")
    print("-" * 50)
    
    
    test_delete_author(author_id)
    

if __name__ == "__main__":
    main()