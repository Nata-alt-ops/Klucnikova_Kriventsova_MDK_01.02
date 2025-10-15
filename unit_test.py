import unittest
import requests
import time
from datetime import date, timedelta


class TestLibraryAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8000"
    
    def setUp(self):
        self.timestamp = int(time.time())
    

    def test_01_get_authors(self):
        response = requests.get(f"{self.BASE_URL}/authors/")
        self.assertEqual(response.status_code, 200)


    def test_02_create_author(self):
        data = {'name': f'Author {self.timestamp}', 'bio': 'Bio'}
        response = requests.post(f"{self.BASE_URL}/authors/", params=data)
        self.assertEqual(response.status_code, 200)

    def test_03_get_genres(self):
        response = requests.get(f"{self.BASE_URL}/genres/")
        self.assertEqual(response.status_code, 200)

    def test_04_create_genre(self):
        data = {'name': f'Genre {self.timestamp}', 'description': 'Desc'}
        response = requests.post(f"{self.BASE_URL}/genres/", params=data)
        self.assertEqual(response.status_code, 200)

    def test_05_get_books(self):
        response = requests.get(f"{self.BASE_URL}/books/")
        self.assertEqual(response.status_code, 200)

    def test_06_create_book(self):
        author_data = {'name': f'Book Author {self.timestamp}', 'bio': 'Bio'}
        author_response = requests.post(f"{self.BASE_URL}/authors/", params=author_data)
        author_id = author_response.json().get('author_id', 1)
        
        genre_data = {'name': f'Book Genre {self.timestamp}', 'description': 'Desc'}
        genre_response = requests.post(f"{self.BASE_URL}/genres/", params=genre_data)
        genre_id = genre_response.json().get('genre_id', 1)
        
        book_data = {
            'title': f'Book {self.timestamp}',
            'author_id': author_id,
            'genre_id': genre_id,
            'isbn': f'999{self.timestamp}',
            'publication_year': 2024,
            'available_copies': 5
        }
        
        response = requests.post(f"{self.BASE_URL}/books/", params=book_data)
        self.assertEqual(response.status_code, 200)

    def test_07_get_readers(self):
        response = requests.get(f"{self.BASE_URL}/readers/")
        self.assertEqual(response.status_code, 200)

    def test_08_create_reader(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': f'john{self.timestamp}@example.com',
            'phone': '+1234567890'
        }
        response = requests.post(f"{self.BASE_URL}/readers/", params=data)
        self.assertEqual(response.status_code, 200)

    def test_09_get_book_loans(self):
        response = requests.get(f"{self.BASE_URL}/book-loans/")
        self.assertEqual(response.status_code, 200)

    def test_10_create_book_loan(self):
        books_response = requests.get(f"{self.BASE_URL}/books/")
        readers_response = requests.get(f"{self.BASE_URL}/readers/")
        
        books = books_response.json()
        readers = readers_response.json()
        
        if (isinstance(books, list) and len(books) > 0 and 
            isinstance(readers, list) and len(readers) > 0):
            
            available_book = None
            for book in books:
                if book.get('available_copies', 0) > 0:
                    available_book = book
                    break
            
            if available_book:
                book_id = available_book['book_id']
                reader_id = readers[0]['reader_id']
                
                loan_data = {
                    'book_id': book_id,
                    'reader_id': reader_id,
                    'loan_date': str(date.today()),
                    'due_date': str(date.today() + timedelta(days=14))
                }
                
                response = requests.post(f"{self.BASE_URL}/book-loans/", params=loan_data)
                self.assertEqual(response.status_code, 200)
            else:
                self.skipTest("Нет доступных книг")
        else:
            self.skipTest("Нет книг или читателей")


if __name__ == '__main__':
    unittest.main()