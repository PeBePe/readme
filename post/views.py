from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from books.models import Book
from post.forms import PostForm
from post.models import Like, Post
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count


def index(request):
    return render(request, 'post/index.html')


@csrf_exempt
def create_post(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user
            post = Post(content=content, user=user, book=book)
            post.save()
            return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
        else:
            return HttpResponseNotFound()
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form, 'book': book})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.pk == post.user.pk:
        is_owner = True
    else:
        is_owner = False

    has_liked = post.likes.filter(user_id=request.user).exists()

    return render(request, 'post/post_detail.html', {'post': post, 'is_owner': is_owner, 'has_liked': has_liked})


def show_json(request):
    data = Like.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_json_by_id(request, post_id):
    data = Post.objects.filter(pk=post_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('post-detail', args=[post_id]))

    context = {'form': form, 'post': post}
    return render(request, "post/edit_post.html", context)


@csrf_exempt
def delete_post(request, post_id):
    if request.method == "DELETE":
        post = Post.objects.get(pk=post_id)
        post.delete()
        return JsonResponse({'redirect_url': reverse('homepage')})
    return HttpResponseNotFound()


@csrf_exempt
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        like_exists = Like.objects.filter(user_id=user, post_id=post).exists()

        if like_exists:
            Like.objects.filter(user_id=user, post_id=post).delete()
        else:
            like = Like(user_id=user, post_id=post)
            like.save()

        likes_count = post.likes.count()

        return JsonResponse({"likes_count": likes_count, "user_has_liked": not like_exists})
    else:
        return HttpResponseNotFound()


@require_http_methods(["GET"])
def api_get_posts(request):
    posts = Post.objects.select_related('user', 'book').annotate(
        like_count=Count('likes')).order_by('-created_at')
    result = [{
        "id": post.id,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "content": post.content,
        "user": {
            "id": post.user.id,
            "username": post.user.username,
            "name": post.user.name,
            "biodata": post.user.biodata
        },
        "book": {
            "id": post.book.id,
            "title": post.book.title,
            "image_url": post.book.image_url,
            "author": post.book.author,
            "publication_date": post.book.publication_date
        },
        "like_count": post.like_count,
    } for post in posts]
    return JsonResponse({"status": True, "message": "Berhasil mendapatkan data posting", "post": result})


@require_http_methods(["GET"])
def api_get_post_detail(request, post_id):
    try:
        data = Post.objects.annotate(
            jumlah_likes=Count('likes')).get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"status": False, "message": "Post tidak ditemukan"}, status=404)

    response_data = {
        "status": True,
        "message": "Success mendapatkan post",
        "post": {
            "content": data.content,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "user": {
                "id": data.user.pk,
                "name": data.user.name,
            },
            "book": {
                "id": data.book.pk,
                "title": data.book.title,
                "author": data.book.author,
                "image_url": data.book.image_url,
                "publication_date": data.book.publication_date,
            },
            "likes_count": data.jumlah_likes,
        }
    }

    return JsonResponse(response_data)


@require_http_methods(["POST"])
@csrf_exempt
def api_create_post(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = PostForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        user = request.user

        if (not user.is_authenticated):
            return JsonResponse({"status": False, "message": "Anda belum login!"}, status=401)

        post = Post(content=content, user=user, book=book)
        post.save()

        result = {
            "id": post.pk,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "content": post.content,
        }
        return JsonResponse({"status": True, "message": "Post berhasil dibuat", "post": result}, status=201)
    return JsonResponse({"status": False, "message": "Data tidak valid"}, status=400)


@require_http_methods(["POST"])
@csrf_exempt
def api_edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"status": False, "message": "Data post tidak ditemukan"}, status=404)

    if (not request.user.is_authenticated):
        return JsonResponse({"status": False, "message": "Anda belum login"}, status=401)

    if (request.user.pk != post.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat mengedit post milik orang lain!"}, status=403)

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid() and request.method == "POST":
        form.save()
        return JsonResponse({"status": True, "message": "Post berhasil diedit"})
    return JsonResponse({"status": False, "message": "Data tidak valid"}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_post(request, post_id):
    if (not request.user.is_authenticated):
        return JsonResponse({"status": False, "message": "Anda belum login"}, status=401)

    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"status": False, "message": "Data post tidak ditemukan"}, status=404)

    if (request.user.pk != post.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat mengedit post milik orang lain!"}, status=403)

    post.delete()
    return JsonResponse({"status": True, "message": "Post berhasil dihapus"})


@require_http_methods(["PUT"])
def api_like_post(request, post_id):
    pass
