"""
URL configuration for readme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('landing-page/', views.landing, name="landing-page"),
    path('', views.index, name="homepage"),
    path('auth/login', views.signin, name='login'),
    path('auth/register', views.register, name='register'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('books/', include("books.urls")),
    path('quotes/', include("quotes.urls")),
    path('post/', include("post.urls")),
    path('shop/', include("shop.urls")),
    path('wishlist/', include('wishlist.urls')),
    path('api/auth/login', views.api_login),
    path('api/auth/register', views.api_register),
    path('api/auth/logout', views.api_logout),
    path('api/profile', views.api_profile),
    path('api/books/', include("books.api_urls")),
    path('api/post/', include("post.api_urls")),
    path('api/shop/', include("shop.api_urls")),
    path('api/quotes/', include("quotes.api_urls")),
    path('api/wishlist/', include("wishlist.api_urls")),
]
