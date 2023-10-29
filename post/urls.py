from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='post'),
    path('<int:post_id>', views.post_detail, name="post-detail"), # Url untuk detail postingan.
    path('create/<int:book_id>', views.create_post, name="create-post"), # Url untuk buat post berdasarkan buku
    path('json', views.show_json, name="show-json"), # Url untuk mendapatkan seluruh postingan dalam bentuk json
    path('json/<int:post_id>', views.show_json_by_id, name="show-json-by-id"), #Url untuk mendapatkan detail positing dalam bentuk json
    path('edit/<int:post_id>', views.edit_post, name="edit-post"), # Url untuk edit post berdasarkan id
    path('delete/<int:post_id>', views.delete_post, name="delete-post"), #Url untuk delete post berdasarkan id
    path('post/like/<int:post_id>/', views.like_post, name='like-post'),
]