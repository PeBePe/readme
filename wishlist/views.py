from django.shortcuts import render
from readme.models import User
from django.http import HttpResponseRedirect
from .forms import WishlistForm
from django.urls import reverse
from .models import Wishlist, Book
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.


def index(request):
    wishlists = request.user.wishlist.all()
    print(wishlists)
    # wishlist = Wishlist.objects.get(id=wishlist_id)
    context = {
        'wishlists': wishlists
    }

    # for wishlist in wishlists :
    #     print(wishlist.note)

    # wishlist = Wishlist.objects.get(id=wishlist_id)
    # wishlist = User.objects.get(id=id).wishlist.all()
    # print(wishlist)

    return render(request, 'wishlist/index.html', context)

# def wishlist_book(request, id) :
#     wishlist = User.objects.get(id=id).wishlist.all()
#     print(wishlist)

#     return render(request, 'wishlist/index.html')


def add(request, book_id):
    # user = request.user
    book = Book.objects.get(pk=book_id)
    form = WishlistForm(request.POST or None)
    if request.method == "POST":
        wishlist = Wishlist(note=request.POST.get('note'),
                            user=request.user, books=book)
        wishlist.save()
        return HttpResponseRedirect(reverse('wishlist'))

    context = {'form': form}
    return render(request, "wishlist/form.html", context)


def remove(request, wishlist_id):
    print(wishlist_id)
    wishlist = Wishlist.objects.get(pk=wishlist_id)
    wishlist.delete()
    return HttpResponseRedirect(reverse('wishlist'))


def edit(request, wishlist_id):

    wishlist = Wishlist.objects.get(pk=wishlist_id)
    form = WishlistForm(instance=wishlist)
    if request.method == "POST":
        wishlist.note = request.POST.get('note')
        wishlist.save()
        return HttpResponseRedirect(reverse('wishlist'))

    context = {'form': form}
    return render(request, "wishlist/form.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def api_add(request, book_id):
    if (not request.user.is_authenticated):
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)
    try:
        book = Book.objects.get(pk=book_id)
    except:
        return JsonResponse(
            {"status": False, "message": "Buku tidak ditemukan"}, status=404)

    if (not request.POST.get('note', False)):
        return JsonResponse(
            {"status": False, "message": "Data yang diberikan tidak valid!"}, status=301)
    form = WishlistForm(request.POST)
    print(form.is_valid)

    wishlist = Wishlist(note=request.POST.get('note'),
                        user=request.user, books=book)
    wishlist.save()

    print(Wishlist)
    wishlist_dict = {
        "id": wishlist.id,
        "wishlist_date": wishlist.wishlist_date,
        "note": wishlist.note,
    }
    return JsonResponse({"status": True, "message": "Success menambahkan wishlist", "wishlist": wishlist_dict}, status=201)


@require_http_methods(["GET"])
def api_get_all(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)

    wishlists = request.user.wishlist.select_related('books')

    wishlists_data = [
        {
            "id": wishlist.id,
            "wishlist_date": wishlist.wishlist_date,
            "note": wishlist.note,
            "user_id": wishlist.user.id,
            "book": {
                "id": wishlist.books.id,
                "title": wishlist.books.title,
                "image_url": wishlist.books.image_url,
            }
        }
        for wishlist in wishlists
    ]

    return JsonResponse({
        "status": True,
        "message": "Success mengambil data wishlist",
        "wishlists": wishlists_data
    })


@require_http_methods(["DELETE"])
@csrf_exempt
def api_remove(request, wishlist_id):
    if (not request.user.is_authenticated):
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)

    try:
        wishlist = Wishlist.objects.get(pk=wishlist_id)
    except:
        return JsonResponse(
            {"status": False, "message": "Wishlist tidak ditemukan"}, status=404)

    if (wishlist.user.id != request.user.id):
        return JsonResponse({"status": False, "message": "Anda tidak dapat menghapus wishlist milik orang lain!"}, status=403)

    wishlist.delete()
    return JsonResponse({"status": True, "message": "Wishlist berhasil dihapus"})


@require_http_methods(["POST"])
@csrf_exempt
def api_edit(request, wishlist_id):
    if (not request.user.is_authenticated):
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)

    try:
        wishlist = Wishlist.objects.get(pk=wishlist_id)
    except:
        return JsonResponse(
            {"status": False, "message": "Wishlist tidak ditemukan"}, status=404)

    if (wishlist.user.id != request.user.id):
        return JsonResponse({"status": False, "message": "Anda tidak dapat mengedit wishlist milik orang lain!"}, status=403)

    new_note = request.POST.get('note')

    if (not new_note):
        return JsonResponse(
            {"status": False, "message": "Data yang diberikan tidak valid!"}, status=301)

    form = WishlistForm(instance=wishlist)
    wishlist.note = new_note
    wishlist.save()

    wishlist_dict = {
        "id": wishlist.id,
        "note": wishlist.note,
    }
    return JsonResponse({"status": True, "message": "Wishlist berhasil diedit", "wishlist": wishlist_dict})
