from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shop.models import ShopItem
from readme.models import User

# Create your views here.

def index(request):
    shop_items = ShopItem.objects.all()
    return render(request, 'shop/index.html', {'shop_items': shop_items})

def show_cart(request):
    cart_items = request.user.shopping_cart.all()
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

def show_bookshelf(request):
    bookshelf = request.user.bookshelf.all()
    return render(request, 'shop/bookshelf.html', {'bookshelf': bookshelf})

def show_item_detail(request, item_id):
    item = ShopItem.objects.get(pk=item_id)
    return render(request, 'shop/shop-item-detail.html', {'item': item})

@csrf_exempt
def add_to_cart(request, item_id):
    if request.method == 'POST':
        item = ShopItem.objects.get(pk=item_id)
        user = User.objects.get(id=request.user.id)
        user.shopping_cart.add(item)
        user.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

def get_shopping_cart_json(request):
    user = User.objects.get(id=request.user.id)
    cart_items = user.shopping_cart.all().values('id', 'amount', 'price', 'book__title', 'book__image_url', 'book__publication_date')
    return HttpResponse(JsonResponse(list(cart_items), safe=False))

@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == 'DELETE':
        user = User.objects.get(id=request.user.id)
        item = user.shopping_cart.get(pk=item_id)
        user.shopping_cart.remove(item)
        user.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        cart_items = user.shopping_cart.all()
        total_price = 0
        for item in cart_items:
            total_price += item.price
        if user.loyalty_point < total_price:
            return HttpResponse(b"NOT ENOUGH LOYALTY POINT", status=400)
        for item in cart_items:
            user.bookshelf.add(ShopItem.objects.get(pk=item.pk))
            shop_item = ShopItem.objects.get(pk=item.pk)
            shop_item.amount -= 1
            shop_item.save()
        user.loyalty_point -= total_price
        user.shopping_cart.clear()
        user.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()