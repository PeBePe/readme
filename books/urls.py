from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='books'),
    path('<int:book_id>', views.book_detail, name="book-detail"),
    path('review/json/<int:book_id>', views.get_review_json, name="review-json"),
    path('add-review/<int:book_id>', views.add_review, name="add-review"),
    path('detele-review/<int:review_id>',
         views.delete_review, name="delete-review"),
    path('edit-page/<int:book_id>/<int:review_id>',
         views.edit_page, name="edit-page"),
]
