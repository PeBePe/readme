from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_get_posts),
    path('<int:post_id>', views.api_get_post_detail),
    path('create/<int:book_id>', views.api_create_post),
    path('edit/<int:post_id>', views.api_edit_post),
    path('delete/<int:post_id>', views.api_delete_post),
    path('post/like/<int:post_id>/', views.api_like_post),
]
