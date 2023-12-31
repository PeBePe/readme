from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('cart/', views.show_cart, name='cart'),
    path('bookshelf/', views.show_bookshelf, name='bookshelf'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/get-shopping-cart-json/', views.get_shopping_cart_json, name='get_shopping_cart_json'),
    path('cart/remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('shop-item/<int:item_id>/', views.show_item_detail, name='item_detail'),
    path('cart/increment-cart-item/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('cart/decrement-cart-item/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
]
