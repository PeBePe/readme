from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_get_shop_items),
    path('cart/', views.api_get_cart_items),
    path('bookshelf/', views.api_get_bookshelf_items),
    path('<int:item_id>/', views.api_get_shop_item_detail),
    path('add-to-cart/<int:item_id>', views.api_add_to_cart),
    path('cart/remove-from-cart/<int:item_id>', views.api_remove_from_cart),
    path('cart/increment-cart-item/<int:item_id>', views.api_increment_cart_item),
    path('cart/decrement-cart-item/<int:item_id>', views.api_decrement_cart_item),
    path('cart/checkout', views.api_checkout),
]
