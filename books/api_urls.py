from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_books, name='books'),
    path('<int:book_id>', views.api_book_detail, name="book-detail"),
    path('review/<int:book_id>',
         views.api_get_review, name="review-json"),
    path('add-review/<int:book_id>', views.api_add_review, name="add-review"),
    path('delete-review/<int:review_id>',
         views.api_delete_review, name="delete-review"),
    path('edit/<int:review_id>',
         views.api_edit_review, name="edit-page"),
]
