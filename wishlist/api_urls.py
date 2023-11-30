from django.urls import path
from . import views

urlpatterns = [

    path('add/<int:book_id>', views.api_add),
    path('', views.api_get_all),
    path('remove/<int:wishlist_id>/', views.api_remove),
    path('edit/<int:wishlist_id>/', views.api_edit),
]
