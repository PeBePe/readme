from django.forms import ModelForm
from shop.models import ShoppingCartItem

class ShoppingCartItemForm(ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ["amount"]