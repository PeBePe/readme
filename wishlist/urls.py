from django.urls import path
from . import views

urlpatterns = [

    path('add/<int:book_id>', views.add, name='add'),
    path('', views.index, name='wishlist'),
    path('remove/<int:wishlist_id>/', views.remove, name='remove'),
    path('edit/<int:wishlist_id>/', views.edit, name='edit'),
]
