from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from readme.forms import RegisterForm, LoginForm, EditUserForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, BadRequest
from post.models import Post
from books.models import Book, Review
from quotes.models import Quote
from django.db.models import Count
from django.core.serializers import serialize
import datetime
import json


@login_required(login_url='/landing-page', redirect_field_name=None)
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    newest_books = Book.objects.order_by('-publication_date')[:3]
    categories = Book.objects.values_list(
        'category', flat=True).distinct()[:15]
    best_quote = Quote.objects.annotate(cited_count=Count(
        'cited_quote')).order_by('-cited_count').first()

    for post in posts:
        post.has_liked = post.likes.filter(user_id=request.user).exists()

    context = {
        'user': request.user,
        'posts': posts,
        "books": newest_books,
        "categories": categories,
        "quote": best_quote
    }
    return render(request, 'readme/index.html', context=context)


def landing(request):
    return render(request, 'readme/landing.html')


@require_http_methods(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            if (len(username) == 0 or len(password) == 0):
                raise BadRequest()
            user = authenticate(request, username=username, password=password)
            if (user is None):
                raise ValidationError(
                    'You have entered incorrect username or password')
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        except ValidationError as err:
            return render(request, 'readme/login.html', {'form': form, 'error': err.message})
        except BadRequest as err:
            return render(request, 'readme/login.html', {'form': form})
    else:
        return render(request, 'readme/login.html')


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            form.save()
            return redirect('login')
        except:
            return render(request, 'readme/register.html', {'form': form})
    else:
        return render(request, 'readme/register.html')


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/landing-page', redirect_field_name=None)
def profile(request):
    context = {
        "user": request.user
    }
    return render(request, 'readme/profile.html', context=context)


@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    if (request.method == 'POST'):

        form = EditUserForm()
        return render(request, 'readme/edit-profile.html', {"form": form})
    else:
        return render(request, 'readme/edit-profile.html', {"form": form})


@csrf_exempt
def api_login(request):
    print(request.POST.get('username'))
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)


@csrf_exempt
def api_register(request):
    form = RegisterForm(request.POST)
    if (form.is_valid()):
        form.save()
        return JsonResponse({
            "status": True,
            "message": "Register berhasil"
        })
    errors_dict = form.errors.as_data()
    formatted_errors = {}

    for field, error_list in errors_dict.items():
        formatted_errors[field] = [error.message for error in error_list]

    return JsonResponse({
        'status': False,
        'message': 'Registrasi gagal',
        'errors': formatted_errors,
    }, status=400)


@require_http_methods(["GET"])
@csrf_exempt
def api_logout(request):
    username = request.user.username
    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout gagal."
        }, status=401)


@require_http_methods(["GET"])
def api_profile(request):
    if request.user.is_authenticated:
        user = request.user

        # Retrieve reviews for the user
        user_reviews = Review.objects.filter(user=user)
        reviews_data = [
            {
                "id": user_review.pk,
                "created_at": user_review.created_at,
                "updated_at": user_review.updated_at,
                "content": user_review.content,
                "book": {
                    "id": user_review.book.id,
                    "title": user_review.book.title,
                    "author": user_review.book.author,
                    "publication_date": user_review.book.publication_date,
                    "image_url": user_review.book.image_url,
                },
            }
            for user_review in user_reviews
        ]
        # Retrieve cited quotes for the user with related user names
        user_cited_quotes = Quote.objects.filter(user=user)
        cited_quotes_data = [
            {
                "id": cited_quote.pk,
                "created_at": cited_quote.created_at,
                "updated_at": cited_quote.updated_at,
                "quote": cited_quote.quote,
                "user": {
                    "id": cited_quote.user.id,
                    "name": cited_quote.user.name,
                }
            }
            for cited_quote in user_cited_quotes
        ]

        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "name": user.name,
            "birthdate": user.birthdate,
            "biodata": user.biodata,
            "phone": user.phone,
            "loyalty_point": user.loyalty_point,
            "quote": user.quote.quote if user.quote else None,
            "cited_quotes": cited_quotes_data,
            "reviews": reviews_data,
        }

        return JsonResponse({
            "status": True,
            "message": "Sukses mendapatkan data profil",
            "user": profile_data
        })
    else:
        return JsonResponse({
            "status": False,
            "message": "Gagal mendapatkan data profil. Pengguna tidak terotentikasi."
        }, status=401)


@require_http_methods(["GET"])
def api_home(request):
    posts = Post.objects.all().order_by('-created_at')
    newest_books = Book.objects.order_by('-publication_date')[:3]
    categories = Book.objects.values_list(
        'category', flat=True).distinct()[:15]
    best_quote = Quote.objects.annotate(cited_count=Count(
        'cited_quote')).order_by('-cited_count').first()

    for post in posts:
        if (request.user.is_authenticated):
            post.has_liked = post.likes.filter(user_id=request.user).exists()
        else:
            post.has_liked = False

    categories = [category for category in categories]

    posts = [{
        "id": post.id,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "content": post.content,
        "user": {
            "id": post.user.id,
            "username": post.user.username,
            "name": post.user.name,
        },
        "book": {
            "id": post.book.id,
            "title": post.book.title,
            "author": post.book.author,
            "publication_date": post.book.publication_date,
            "image_url": post.book.image_url,
        },
        # "like_count": post.likes,
    } for post in posts]

    best_quote = {
        "quote": best_quote.quote if best_quote else "",
        "author": best_quote.user.name if best_quote else ""
    }
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data", "posts": posts, "newest_books": list(newest_books.values()), "categories": list(categories), "best_quote": best_quote})
