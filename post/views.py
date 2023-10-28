from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from books.models import Book
from post.forms import PostForm
from post.models import Like, Post
from django.views.decorators.csrf import csrf_exempt

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
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return HttpResponseNotFound()
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', { 'form' : form, 'book': book})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.user.pk == post.user.pk:
        is_owner = True
    else:
        is_owner = False

    has_liked = post.likes.filter(user_id=request.user).exists()

    return render(request, 'post/post_detail.html', {'post': post, 'is_owner': is_owner, 'has_liked': has_liked})


def show_json(request):
    data = Post.objects.all()
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
        if request.user == post.user:
            post.delete()
            return HttpResponseRedirect(reverse('homepage'))
        
@csrf_exempt
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        # Periksa apakah pengguna sudah memberikan like pada post
        if post.likes.filter(user=user).exists():
            return JsonResponse({"error": "Anda sudah memberikan like pada post ini."})

        # Tambahkan like
        like = Like(user=user, post=post)
        like.save()

        like_count = post.likes.count()

        return JsonResponse({"success": True, "like_count": like_count})

    return JsonResponse({"error": "Metode tidak diizinkan."})