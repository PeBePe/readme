from django.forms import ModelForm
from quotes.models import Quote


class ProductForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["quote"]
