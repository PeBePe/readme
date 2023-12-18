from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.core import serializers
from django.db.models import Q, Count
from .models import Book, Review
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    q = request.GET.get('q', '')
    field = request.GET.get('field', '')
    category = request.GET.get('category', '')
    books = Book.objects.all()

    if q:
        q_filter = Q(title__icontains=q) | Q(
            author__icontains=q) | Q(publisher__icontains=q)
        books = books.filter(q_filter)
    if field in ['title', 'author', 'publisher']:
        field_filter = {f'{field}__icontains': q}
        books = books.filter(**field_filter)
    if category:
        books = books.filter(category=category)

    categories = Book.objects.values('category').distinct()
    return render(request, 'books/index.html', {"books": books, "categories": categories})


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)

    context = {
        "book": book,
        "user": request.user
    }
    return render(request, 'books/detail.html', context)


def get_review_json(request, book_id):
    reviews = Review.objects.filter(book=book_id).values(
        'id', 'content', 'created_at', 'updated_at', 'user__name', 'user__biodata', 'user__username', 'user__id')

    formatted_reviews = []
    for review in reviews:
        formatted_reviews.append({
            "id": review["id"],
            "content": review["content"],
            "created_at": review["created_at"].strftime("%d/%m/%y"),
            "updated_at": review["updated_at"].strftime("%d/%m/%y"),
            "user": {
                "id": review["user__id"],
                "name": review["user__name"],
                "username": review["user__username"],
                "biodata": review["user__biodata"],
            }
        })

    return HttpResponse(JsonResponse(formatted_reviews, safe=False))


def add_review(request, book_id):
    book = Book.objects.get(pk=book_id)
    user = request.user

    new_review = Review(book=book, content=request.POST.get(
        'content'), user=request.user)
    new_review.save()

    user.loyalty_point += 100
    user.save()
    return HttpResponse(serializers.serialize("json", [new_review]), content_type="application/json")


def delete_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    user = request.user

    review.delete()

    user.loyalty_point -= 100
    user.save()
    return HttpResponseRedirect(reverse('book-detail', kwargs={'book_id': review.book.pk}))


def edit_page(request, book_id, review_id):
    if (request.method == 'POST'):
        review = Review.objects.get(pk=review_id)
        review.content = request.POST.get('content')
        review.save()
        return HttpResponseRedirect(reverse('book-detail', kwargs={'book_id': book_id}))
    else:
        book = Book.objects.get(pk=book_id)
        review = Review.objects.get(pk=review_id)

        context = {
            "book": book,
            "review": review
        }
        return render(request, 'books/edit.html', context)


@require_http_methods(["GET"])
def api_books(request):
    q = request.GET.get('q', '')
    field = request.GET.get('field', '')
    category = request.GET.get('category', '')
    books = Book.objects.all()

    if q:
        q_filter = Q(title__icontains=q) | Q(
            author__icontains=q) | Q(publisher__icontains=q)
        books = books.filter(q_filter)
    if field in ['title', 'author', 'publisher']:
        field_filter = {f'{field}__icontains': q}
        books = books.filter(**field_filter)
    if category:
        books = books.filter(category=category)

    # Annotate the books queryset with the count of reviews for each book
    books = books.annotate(review_count=Count('reviews'))

    categories = [category.get('category') for category in Book.objects.values(
        'category').distinct()]

    # Create a list of dictionaries with book information and review count
    books_data = [
        {
            'id': book.pk,
            'isbn': book.isbn,
            'title': book.title,
            'description': book.description,
            'author': book.author,
            'publisher': book.publisher,
            'publication_date': book.publication_date,
            'page_count': book.page_count,
            'category': book.category,
            'image_url': book.image_url,
            'lang': book.lang,
            'review_count': book.review_count,
        }
        for book in books
    ]

    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data buku", "books": books_data, "categories": list(categories)})


@require_http_methods(["GET"])
def api_book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    book_data = {
        'id': book.id,
        'isbn': book.isbn,
        'title': book.title,
        'description': book.description,
        'author': book.author,
        'publisher': book.publisher,
        'publication_date': str(book.publication_date),
        'page_count': book.page_count,
        'category': book.category,
        'image_url': book.image_url,
        'lang': book.lang,
    }
    user = {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "created_at": request.user.created_at,
        "updated_at": request.user.updated_at,
        "name": request.user.name,
        "birthdate": request.user.birthdate,
        "biodata": request.user.biodata,
        "phone": request.user.phone,
        "loyalty_point": request.user.loyalty_point,
    } if request.user.is_authenticated else None
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan detail buku", "book": book_data, "user": user})


@require_http_methods(["GET"])
def api_get_review(request, book_id):
    reviews = Review.objects.filter(book=book_id).values(
        'id', 'content', 'created_at', 'updated_at', 'user__name', 'user__biodata', 'user__username', 'user__id')

    formatted_reviews = []
    for review in reviews:
        formatted_reviews.append({
            "id": review["id"],
            "content": review["content"],
            "created_at": review["created_at"].strftime("%d/%m/%y"),
            "updated_at": review["updated_at"].strftime("%d/%m/%y"),
            "user": {
                "id": review["user__id"],
                "name": review["user__name"],
                "username": review["user__username"],
                "biodata": review["user__biodata"],
            }
        })

    return HttpResponse(JsonResponse({"status": True, "message": "Berhasil mendapatkan review buku", "reviews": formatted_reviews}))


@csrf_exempt
@require_http_methods(["POST"])
def api_add_review(request, book_id):
    book = Book.objects.get(pk=book_id)
    if (not request.user.is_authenticated):
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)
    user = request.user

    if (not request.POST.get('content', False)):
        return JsonResponse(
            {"status": False, "message": "Content tidak boleh kosong!"}, status=400)

    new_review = Review(book=book, content=request.POST.get(
        'content'), user=request.user)

    new_review.save()

    user.loyalty_point += 100
    user.save()
    return HttpResponse(serializers.serialize("json", [new_review]), content_type="application/json")


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"status": False, "message": "Review tidak ditemukan"}, status=404)

    user = request.user

    if (user.pk != review.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat menghapus review orang lain"}, status=403)

    review.delete()

    user.loyalty_point -= 100
    user.save()
    return JsonResponse({"status": True, "message": "Berhasil menghapus review"}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def api_edit_review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"status": False, "message": "Review tidak ditemukan"}, status=404)

    user = request.user

    if (user.pk != review.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat mengedit review orang lain"}, status=403)
    new_content = request.POST.get('content', False)
    if (not new_content):
        return JsonResponse(
            {"status": False, "message": "Content tidak boleh kosong!"}, status=400)

    review.content = new_content
    review.save()
    return JsonResponse({"status": True, "message": "Berhasil mengedit review"}, status=200)
