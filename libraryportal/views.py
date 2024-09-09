from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import requests
from requests.exceptions import RequestException
def home(request):
    return render(request,'home.html',context={"current_tab": "home"})

def reader(request):
    return render(request,'readers.html', context={"current_tab":"reader"})


def shopping(request):
    return HttpResponse('Welcome to shopping')


def save_student(request):
    student_name= request.POST['student_name']
    return render(request, "welcome.html", context={'student_name' : student_name})


def readers_tab(request):
    if request.method=="GET":
        readers = Reader.objects.all()
        return render(request,"readers.html", context={"current_tab": "readers", "readers": readers})
    else:
        query = request.POST['query']
        readers = Reader.objects.raw("select * from libraryportal_Reader where reader_name like '%"+query+"%'")
        return render(request, "readers.html", context={"current_tab": "readers", "readers": readers, "query": query})



def save_reader(request):
    reader_item = Reader(reference_id= request.POST['reader_reference'],
                         reader_name = request.POST['reader_name'],
                         reader_contact = request.POST['reader_contact'],
                         reader_address = request.POST['reader_address'],
                         active= True
                         )
    reader_item.save()
    return redirect('/readers')




from django.shortcuts import render, redirect
from django.conf import settings
from .models import BorrowedBook
import requests
from requests.exceptions import RequestException

def books_tab(request):
    if request.method == "POST":
        if 'query' in request.POST:
            query = request.POST.get('query', '')
            try:
                response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query}")
                response.raise_for_status()
                books = response.json().get('items', [])
            except RequestException as e:
                print(f"Error fetching books: {e}")
                books = []
        elif 'borrow' in request.POST:
            book_id = request.POST.get('book_id')
            book_title = request.POST.get('book_title')
            reference_id = request.POST.get('reference_id')

            # Save the borrowed book in the database
            BorrowedBook.objects.create(reference_id=reference_id, book_id=book_id, book_title=book_title)

            # Redirect to the books page after borrowing
            return redirect('books_tab')
    else:
        books = []
        query = 'programming'  # Default query on initial load

    return render(request, 'books.html', context={"current_tab": "books", "books": books})







def add_to_bag(request, book_id):
    book_data = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}").json()
    title = book_data['volumeInfo'].get('title', 'Unknown Title')
    author = book_data['volumeInfo'].get('authors', ['Unknown Author'])[0]
    isbn = book_data['volumeInfo'].get('industryIdentifiers', [{}])[0].get('identifier', 'N/A')

    book, created = Book.objects.get_or_create(
        title=title, author=author, isbn=isbn, defaults={'available': True}
    )

    reader = Reader.objects.first()  # Replace with the correct logic for the logged-in user
    BorrowedBook.objects.create(reader=reader, book=book)

    return redirect('/mybag')

from django.shortcuts import render
from .models import BorrowedBook

def my_bag(request):
    if request.method == "POST":
        reference_id = request.POST.get('reference_id', '')
        borrowed_books = BorrowedBook.objects.filter(reference_id=reference_id, returned=False)
    else:
        borrowed_books = []

    return render(request, 'mybag.html', context={"current_tab": "mybag", "borrowed_books": borrowed_books})

from django.shortcuts import render
from .models import BorrowedBook

def returns_tab(request):
    if request.method == "POST":
        reference_id = request.POST.get('reference_id', '')
        borrowed_books = BorrowedBook.objects.filter(reference_id=reference_id, returned=False)
    else:
        borrowed_books = []

    return render(request, 'returns.html', context={"current_tab": "returns", "borrowed_books": borrowed_books})


def return_books(request):
    borrowed_books = []
    if request.method == "POST":
        reference_id = request.POST.get('reference_id')
        borrowed_books = BorrowedBook.objects.filter(reference_id=reference_id, returned=False)

        if 'return' in request.POST:
            book_id = request.POST.get('book_id')
            borrowed_book = BorrowedBook.objects.get(reference_id=reference_id, book_id=book_id, returned=False)
            borrowed_book.returned = True
            borrowed_book.save()
            return redirect('return_books')

    return render(request, 'return_books.html', context={"current_tab": "return", "borrowed_books": borrowed_books})
