from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('readers/', views.readers_tab),
    path('shop/', views.shopping),
    path('save',views.save_student),
    path('readers/add', views.save_reader),

    path('books/add_to_bag/<str:book_id>/', views.add_to_bag, name='add_to_bag'),
    path('mybag/', views.my_bag),
    path('returns/', views.returns_tab),
    path('books/', views.books_tab, name='books_tab'),
    path('return/', views.return_books, name='return_books'),


]