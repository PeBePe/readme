from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_books),
    path('<int:book_id>', views.api_book_detail),
    path('review/<int:book_id>', views.api_get_review),
    path('add-review/<int:book_id>', views.api_add_review),
    path('delete-review/<int:review_id>', views.api_delete_review),
    path('edit/<int:review_id>', views.api_edit_review),
]
