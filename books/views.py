from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.db.models import Q
from .models import Book, Review
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
