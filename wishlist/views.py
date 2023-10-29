from django.shortcuts import render
from readme.models import User
from django.http import HttpResponseRedirect
from .forms import WishlistForm
from django.urls import reverse
from .models import Wishlist, Book

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
        wishlist = Wishlist(note=request.POST.get('note'), user=request.user, books=book)
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