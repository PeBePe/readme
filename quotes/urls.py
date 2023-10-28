from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('', views.index, name='quotes'),
    path('create-quotes/', views.create_quotes, name="create-quotes"),
    path('landing-page/', views.landing, name="landing-page"),
    path('delete-quote/<int:id>/', views.delete_quote, name='delete-quote'),
    path('edit-quote/<int:id>/', views.edit_quote, name='edit-quote'),
    path('cited-quote/<int:id>/', views.cited_quote, name='cited-quote'),
]
