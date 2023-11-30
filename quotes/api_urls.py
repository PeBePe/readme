from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_get_quotes),
    path('create-quotes/', views.api_create_quote),
    path('delete-quote/<int:quote_id>/', views.api_delete_quote),
    path('edit-quote/<int:quote_id>/', views.api_edit_quote),
    path('cited-quote/<int:quote_id>/', views.api_cite_quote),
]
