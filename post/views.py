from django.shortcuts import render
from books.models import Book
# Create your views here.
# path('', views.index, name='post'),
# path('<int:post_id>', views.post_detail, name="post-detail"), # Url untuk detail postingan.
# path('create/<int:book_id>', views.create_post, name="create-post"), # Url untuk buat post berdasarkan buku
# path('json', views.show_json, name="show-json"), # Url untuk mendapatkan seluruh postingan dalam bentuk json
# path('json/<int:post_id>', views.show_json_by_id, name="show-json-by-id"), #Url untuk mendapatkan detail positing dalam bentuk json
# path('edit/<int:post_id>', views.edit_post, name="edit-post"), # Url untuk edit post berdasarkan id
# path('delete/<int:post_id>', views.delete_post, name=


def index(request):
    return render(request, 'post/index.html')


def create_book(request, id_buku):
    book = Book.objects.get(pk=id_buku)
    print(book)
    return render(request, 'post/index.html')


def post_detail(request, post_id):
    pass


def create_post(request, book_id):
    pass


def show_json(request):
    pass


def show_json_by_id(request, post_id):
    pass


def edit_post(request, post_id):
    pass


def delete_post(request, post_id):
    pass
