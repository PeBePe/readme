from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from shop.forms import ShoppingCartItemForm
from shop.models import ShopItem, ShoppingCartItem, BookshelfItem
from readme.models import User
from django.views.decorators.http import require_http_methods

# Create your views here.

def index(request):
    q = request.GET.get('q', '')
    price_range = request.GET.get('pricerange', '')
    shop_items = ShopItem.objects.all()

    if q:
        q_filter = Q(book__title__icontains=q) | Q(
            book__author__icontains=q) | Q(book__publisher__icontains=q)
        shop_items = shop_items.filter(q_filter)
    if price_range:
        price_range = price_range.split('-')
        price_range = [int(price) for price in price_range]
        shop_items = shop_items.filter(price__range=price_range)

    return render(request, 'shop/index.html', {'shop_items': shop_items})

@login_required
def show_cart(request):
    cart_items = User.objects.get(pk=request.user.id).shopping_cart.all()
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

@login_required
def show_bookshelf(request):
    bookshelf = User.objects.get(pk=request.user.id).bookshelf.all()
    total_amount = 0
    for book in bookshelf:
        total_amount += book.amount
    return render(request, 'shop/bookshelf.html', {'bookshelf': bookshelf, 'total_amount': total_amount})

def show_item_detail(request, item_id):
    item = ShopItem.objects.get(pk=item_id)
    form = ShoppingCartItemForm(request.POST)
    if (request.method == 'POST' and form.is_valid()) :
        amount = form.cleaned_data['amount']
        cart_item, created = ShoppingCartItem.objects.get_or_create(item=item, user=request.user)
        if created:
            cart_item.amount = amount
        elif cart_item.amount + amount > item.amount:
            return HttpResponse(b"NOT ENOUGH ITEM", status=400)
        cart_item.amount = amount if created else cart_item.amount + amount
        cart_item.save()
        cart_items = User.objects.get(pk=request.user.id).shopping_cart.all()
        return render(request, 'shop/cart.html', {'cart_items': cart_items})
    return render(request, 'shop/shop-item-detail.html', {'item': item, 'form': form})

@login_required
@csrf_exempt
def add_to_cart(request, item_id):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 1))
        shop_item = ShopItem.objects.get(pk=item_id)
        user = User.objects.get(id=request.user.id)
        cart_item, created = ShoppingCartItem.objects.get_or_create(item=shop_item, user=user)
        if created:
            cart_item.amount = amount
        elif cart_item.amount + amount > shop_item.amount:
            return HttpResponse(b"NOT ENOUGH ITEM", status=400)
        cart_item.amount = amount if created else cart_item.amount + amount
        cart_item.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

@login_required
@csrf_exempt
def increment_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        if cart_item.amount + 1 <= cart_item.item.amount:
            cart_item.amount += 1
            cart_item.save()
            return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

@login_required
@csrf_exempt
def decrement_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        cart_item.amount -= 1
        if cart_item.amount < 0:
            cart_item.amount = 0
        cart_item.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

def get_shopping_cart_json(request):
    if request.method == 'GET':
        cart_items = User.objects.get(pk=request.user.id).shopping_cart.all().values('id', 'amount', 'item', 'item__price', 'item__book__title', 'item__book__image_url', 'item__book__publication_date')
        return HttpResponse(JsonResponse(list(cart_items), safe=False))
    return HttpResponseNotFound()

@login_required
@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == 'DELETE':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        cart_item.delete()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

@login_required
@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        cart_items = user.shopping_cart.all()
        total_price = 0
        for cart_item in cart_items:
            total_price += cart_item.item.price * cart_item.amount
        if total_price == 0:
            return HttpResponse(b"EMPTY CART", status=400)
        if user.loyalty_point < total_price:
            return HttpResponse(b"NOT ENOUGH LOYALTY POINT", status=402)
        for cart_item in cart_items:
            if cart_item.amount != 0:
                shop_item = ShopItem.objects.get(pk=cart_item.item.id)
                bookshelf_item, created = BookshelfItem.objects.get_or_create(item=shop_item, user=user)
                bookshelf_item.amount = cart_item.amount if created else bookshelf_item.amount + cart_item.amount
                bookshelf_item.save()
                shop_item.amount -= cart_item.amount
                cart_item.delete()
                shop_item.save()
        user.loyalty_point -= total_price
        user.save()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound()

@require_http_methods(["GET"])
def api_get_shop_items(request):
    q = request.GET.get('q', '')
    price_range = request.GET.get('pricerange', '')
    shop_items = ShopItem.objects.all()

    if q:
        q_filter = Q(book__title__icontains=q) | Q(
            book__author__icontains=q) | Q(book__publisher__icontains=q)
        shop_items = shop_items.filter(q_filter)
    if price_range:
        price_range = price_range.split('-')
        price_range = [int(price) for price in price_range]
        shop_items = shop_items.filter(price__range=price_range)

    result = [{
        'id': shop_item.id,
        'price': shop_item.price,
        'amount': shop_item.amount,
        'book': {
            'id': shop_item.book.id,
            'isbn': shop_item.book.isbn,
            'title': shop_item.book.title,
            'description': shop_item.book.description,
            'author': shop_item.book.author,
            'publisher': shop_item.book.publisher,
            'publication_date': str(shop_item.book.publication_date),
            'page_count': shop_item.book.page_count,
            'category': shop_item.book.category,
            'image_url': shop_item.book.image_url,
            'lang': shop_item.book.lang,
        }
    } for shop_item in shop_items]

    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data shop items", "shop_items": result})

@require_http_methods(["GET"])
def api_get_cart_items(request):
    cart_items = User.objects.get(pk=request.user.id).shopping_cart.all()
    result = [{
        'id': cart_item.id,
        'amount': cart_item.amount,
        'item': {
            'id': cart_item.item.id,
            'price': cart_item.item.price,
            'amount': cart_item.item.amount,
            'book': {
                'id': cart_item.item.book.id,
                'isbn': cart_item.item.book.isbn,
                'title': cart_item.item.book.title,
                'description': cart_item.item.book.description,
                'author': cart_item.item.book.author,
                'publisher': cart_item.item.book.publisher,
                'publication_date': str(cart_item.item.book.publication_date),
                'page_count': cart_item.item.book.page_count,
                'category': cart_item.item.book.category,
                'image_url': cart_item.item.book.image_url,
                'lang': cart_item.item.book.lang,
            }
        }
    } for cart_item in cart_items]
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data cart items", "cart_items": result})

@require_http_methods(["GET"])
def api_get_bookshelf_items(request):
    bookshelf_items = User.objects.get(pk=request.user.id).bookshelf.all()
    result = [{
        'id': bookshelf_item.id,
        'amount': bookshelf_item.amount,
        'item': {
            'id': bookshelf_item.item.id,
            'price': bookshelf_item.item.price,
            'amount': bookshelf_item.item.amount,
            'book': {
                'id': bookshelf_item.item.book.id,
                'isbn': bookshelf_item.item.book.isbn,
                'title': bookshelf_item.item.book.title,
                'description': bookshelf_item.item.book.description,
                'author': bookshelf_item.item.book.author,
                'publisher': bookshelf_item.item.book.publisher,
                'publication_date': str(bookshelf_item.item.book.publication_date),
                'page_count': bookshelf_item.item.book.page_count,
                'category': bookshelf_item.item.book.category,
                'image_url': bookshelf_item.item.book.image_url,
                'lang': bookshelf_item.item.book.lang,
            }
        }
    } for bookshelf_item in bookshelf_items]
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data bookshelf items", "bookshelf_items": result})

@require_http_methods(["GET"])
def api_get_shop_item_detail(request, item_id):
    shop_item = ShopItem.objects.get(pk=item_id)
    shop_item_data = {
        'id': shop_item.id,
        'price': shop_item.price,
        'amount': shop_item.amount,
        'book': {
            'id': shop_item.book.id,
            'isbn': shop_item.book.isbn,
            'title': shop_item.book.title,
            'description': shop_item.book.description,
            'author': shop_item.book.author,
            'publisher': shop_item.book.publisher,
            'publication_date': str(shop_item.book.publication_date),
            'page_count': shop_item.book.page_count,
            'category': shop_item.book.category,
            'image_url': shop_item.book.image_url,
            'lang': shop_item.book.lang,
        }
    }
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data shop item", "shop_item": shop_item_data})

@csrf_exempt
def api_add_to_cart(request, item_id):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 1))
        shop_item = ShopItem.objects.get(pk=item_id)
        user = User.objects.get(id=request.user.id)
        cart_item, created = ShoppingCartItem.objects.get_or_create(item=shop_item, user=user)
        if created:
            cart_item.amount = amount
        elif cart_item.amount + amount > shop_item.amount:
            return JsonResponse({"status": False, "message": "Not enough item"}, status=400)
        cart_item.amount = amount if created else cart_item.amount + amount
        cart_item.save()
        return JsonResponse({"status": True, "message": "Book added to cart successfully!"}, status=200)
    else:
        return JsonResponse({"status": False, "message": "Failed to add book to the cart"}, status=401)
    
@csrf_exempt
def api_remove_from_cart(request, item_id):
    if request.method == 'DELETE':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({"status": True, "message": "Book removed from the cart successfully!"}, status=200)
    else:
        return JsonResponse({"status": False, "message": "Failed to remove book from the cart"}, status=401)

@csrf_exempt
def api_increment_cart_item(request, item_id):
    if request.method == 'PUT':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        if cart_item.amount + 1 <= cart_item.item.amount:
            cart_item.amount += 1
            cart_item.save()
            return JsonResponse({"status": True, "message": "Increment successful!"}, status=200)
        else:
            return JsonResponse({"status": False, "message": "Increment failed"}, status=400)
    else:
        return JsonResponse({"status": False, "message": "Increment failed"}, status=401)
    
@csrf_exempt
def api_decrement_cart_item(request, item_id):
    if request.method == 'PUT':
        cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        cart_item.amount -= 1
        if cart_item.amount < 0:
            cart_item.amount = 0
        cart_item.save()
        return JsonResponse({"status": True, "message": "Decrement successful!"}, status=200)
    else:
        return JsonResponse({"status": False, "message": "Decrement failed"}, status=401)
    
@csrf_exempt
def api_checkout(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        cart_items = user.shopping_cart.all()
        total_price = 0
        for cart_item in cart_items:
            total_price += cart_item.item.price * cart_item.amount
        if total_price == 0:
            return JsonResponse({"status": False, "message": "Your cart is empty"}, status=400)
        if user.loyalty_point < total_price:
            print(user.loyalty_point)
            return JsonResponse({"status": False, "message": "Not enough loyalty points"}, status=402)
        for cart_item in cart_items:
            if cart_item.amount != 0:
                shop_item = ShopItem.objects.get(pk=cart_item.item.id)
                bookshelf_item, created = BookshelfItem.objects.get_or_create(item=shop_item, user=user)
                bookshelf_item.amount = cart_item.amount if created else bookshelf_item.amount + cart_item.amount
                bookshelf_item.save()
                shop_item.amount -= cart_item.amount
                cart_item.delete()
                shop_item.save()
        user.loyalty_point -= total_price
        user.save()
        return JsonResponse({"status": True, "message": "Checkout successful!"}, status=200)
    else:
        return JsonResponse({"status": False, "message": "Checkout failed"}, status=401)