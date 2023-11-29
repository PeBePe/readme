from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='post'),
    path('q<int:post_id>', views.post_detail, name="post-detail"),
    path('create/<int:book_id>', views.create_post, name="create-post"),
    path('json', views.show_json, name="show-json"),
    path('json/<int:post_id>', views.show_json_by_id, name="show-json-by-id"),
    path('edit/<int:post_id>', views.edit_post, name="edit-post"),
    path('delete/<int:post_id>', views.delete_post, name="delete-post"),
    path('post/like/<int:post_id>/', views.like_post, name='like-post'),
]
