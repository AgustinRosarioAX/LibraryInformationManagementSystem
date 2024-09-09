from django.db import models

class Reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id= models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=200)
    reader_address = models.TextField()
    active= models.BooleanField(default=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BorrowedBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.reader.reader_name}"


from django.db import models

class BorrowedBook(models.Model):
    reference_id = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100)
    book_title = models.CharField(max_length=255)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_title} (Borrowed by: {self.reference_id})"
