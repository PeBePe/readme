import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quotes.models import Quote, QuoteCited
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from quotes.forms import ProductForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from readme.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from .serializers import QuoteSerializer

# Create your views here.


# biar main cuma bisa diakses sama user yang udah login
@login_required(login_url='/landing-page', redirect_field_name=None)
def index(request):
    user = request.user
    quotes = Quote.objects.all()  # ambil semua quotes yang ada
    quotes_count = quotes.count()  # menghitung jumlah quotes yang ada
    # ngambil daftar kutipan dan pengguna yang mengutipnya
    quoted_quotes = QuoteCited.objects.select_related(
        'quote_id', 'user_id').all()

    context = {
        'name': request.user.username,
        'user': user,
        'quotes': quotes,
        'quotes_count': quotes_count,
        'quoted_quotes': quoted_quotes
    }

    return render(request, 'quotes/index.html', context)


def landing(request):
    return render(request, 'readme/landing.html')


def create_quotes(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":  # validasi isi form
        quotes = Quote.objects.filter(user=request.user)
        if (quotes):
            return render(request, 'quotes/create_quotes.html', {'form': form, 'error': 'Anda sudah pernah membuat quotes!'})
        # biar objek ga langsung disimpen di database
        quote = form.save(commit=False)
        quote.user = request.user
        quote.save()
        return HttpResponseRedirect(reverse('quotes'))

    context = {'form': form}

    return render(request, 'quotes/create_quotes.html', context)


def delete_quote(request, id):
    if request.method == "POST":
        product = get_object_or_404(Quote, pk=id)
        product.delete()
        return redirect('quotes')


def edit_quote(request, id):
    product = Quote.objects.get(pk=id)

    # set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # form disimpan dan balik ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('quotes'))

    context = {'form': form}
    return render(request, "quotes/edit_quotes.html", context)


def cited_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)

    # Menghitung berapa banyak user yg telah mengutip suatu quote
    cited_count = QuoteCited.objects.filter(quote_id=quote).count()

    # cek apakah user udah cited suatu quote atau belum
    user_cited = QuoteCited.objects.filter(
        quote_id=quote, user_id=request.user).exists()

    if request.method == "POST":
        # cek jumlah cited udah lebih dari 3 atau belum
        if not user_cited and cited_count <= 3:
            QuoteCited.objects.create(quote_id=quote, user_id=request.user)
            cited_count += 1  # tambah jumlah cited quote

    # Mendapatkan daftar kutipan yang sudah dikutip oleh pengguna
    quoted_quotes = Quote.objects.filter(cited_quote__user_id=request.user)

    context = {
        'quote': quote,
        'cited_count': cited_count,
        'user_cited': user_cited,
        'quoted_quotes': quoted_quotes
    }

    # Temukan pemilik kutipan yang dikutip
    quote_owner = quote.user

    if quote_owner:
        # Perbarui poin loyalitas pemilik kutipan
        quote_owner.loyalty_point += 100
        quote_owner.save()
        return redirect('quotes')

    return render(request, 'quotes/cited_quote.html', context)


def search_quotes(request):
    search_value = request.GET.get('search_value', '')

    # Melakukan pencarian berdasarkan judul atau isi kutipan yang sesuai
    quotes = Quote.objects.filter(Q(quote__icontains=search_value) | Q(
        user__username__icontains=search_value))

    # Mengambil hasil pencarian dalam bentuk dictionary
    search_results = [{'quote': quote.quote,
                       'user': quote.user.username} for quote in quotes]

    return JsonResponse({'search_results': search_results})

    # return JsonResponse({'error': 'AJAX ga valid'})


@require_http_methods(["GET"])
def api_get_quotes(request):
    user = request.user
    quotes = Quote.objects.select_related(
        'user')  # ambil semua quotes yang ada
    quotes_count = quotes.count()  # menghitung jumlah quotes yang ada
    # ngambil daftar kutipan dan pengguna yang mengutipnya
    quoted_quotes = QuoteCited.objects.select_related(
        'quote_id', 'user_id').all().values()
    
     # Tambahkan username ke setiap quote
    for quote in quotes:
        #user_id = quote['user']
        user_id = quote.get('user', None)
        try:
            username = User.objects.get(id=user_id).username
            quote['username'] = username
        except User.DoesNotExist:
            # Handle exception jika user_id tidak ditemukan
            quote['username'] = None

    quotes = [{
        "id": quote.id,
        "created_at": quote.created_at,
        "updated_at": quote.updated_at,
        "quote": quote.quote,
        "user_id": quote.user.id,
        "username": quote.user.username
    } for quote in quotes]

    context = {
        'name': request.user.username,
        # 'user': user,
        'quotes': list(quotes),
        'quotes_count': int(quotes_count),
        'quoted_quotes': list(quoted_quotes)
    }

    return JsonResponse({"status": True, "message": "Berhasil mengambil semua data quotes", "data": context})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_quote(request):
    if (not request.user.is_authenticated):
        return JsonResponse(
            {"status": False, "message": "Anda belum melakukan login"}, status=401)

    form = ProductForm(request.POST or None)

    quotes = Quote.objects.filter(user=request.user)
    if (quotes):
        return JsonResponse({"status": False, "message": "Anda sudah pernah membuat quote sebelumnya!"}, status=409)

    # biar objek ga langsung disimpen di database
    quote = form.save(commit=False)
    quote.user = request.user
    quote.save()
    print(quote.__dict__)
    return JsonResponse({"status": True, "message": "Quote berhasil dibuat!", "quote": None}, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_quote(request, quote_id):
    if (not request.user.is_authenticated):
        return JsonResponse({"status": False, "message": "Anda belum login"}, status=401)

    try:
        product = Quote.objects.get(pk=quote_id)
    except:
        return JsonResponse({"status": False, "message": "Data quote tidak ditemukan"}, status=404)

    if (request.user.pk != product.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat menghapus quote milik orang lain!"}, status=403)

    product.delete()
    return JsonResponse({"status": True, "message": "Quote berhasil dihapus"})


@csrf_exempt
@require_http_methods(["POST"])
def api_edit_quote(request, quote_id):
    if (not request.user.is_authenticated):
        return JsonResponse({"status": False, "message": "Anda belum login"}, status=401)

    try:
        product = Quote.objects.get(pk=quote_id)
    except:
        return JsonResponse({"status": False, "message": "Data quote tidak ditemukan"}, status=404)

    if (request.user.pk != product.user.pk):
        return JsonResponse({"status": False, "message": "Anda tidak dapat mengedit quote milik orang lain!"}, status=403)

    # set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)
    if (not form.is_valid()):
        return JsonResponse({"status": False, "message": "Data tidak valid"}, status=400)

    quote_dict = {
        "id": product.pk,
        'created_at': product.created_at,
        'updated_at': product.updated_at,
        "quote": product.quote
    }

    form.save()
    return JsonResponse({"status": True, "message": "Quote berhasil diedit!", "quote": quote_dict}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def api_cite_quote(request, quote_id):
    if (not request.user.is_authenticated):
        return JsonResponse({"status": False, "message": "Anda belum login"}, status=401)

    try:
        quote = Quote.objects.get(pk=quote_id)
    except:
        return JsonResponse({"status": False, "message": "Data quote tidak ditemukan"}, status=404)

    # Menghitung berapa banyak user yg telah mengutip suatu quote
    cited_count = QuoteCited.objects.filter(quote_id=quote).count()

    # cek apakah user udah cited suatu quote atau belum
    user_cited = QuoteCited.objects.filter(
        quote_id=quote, user_id=request.user).exists()

    # cek jumlah cited udah lebih dari 3 atau belum
    if not user_cited and cited_count <= 3:
        QuoteCited.objects.create(quote_id=quote, user_id=request.user)
        cited_count += 1  # tambah jumlah cited quote

    # Mendapatkan daftar kutipan yang sudah dikutip oleh pengguna
    quoted_quotes = Quote.objects.filter(cited_quote__user_id=request.user)
    context = {
        'quote': {
            "id": quote.pk,
            'created_at': quote.created_at,
            'updated_at': quote.updated_at,
            "quote": quote.quote
        },
        'cited_count': int(cited_count),
        'user_cited': user_cited,
        'quoted_quotes': [{
            "id": quote.id,
            'created_at': quote.created_at,
            'updated_at': quote.updated_at,
            "quote": quote.quote
        } for quote in quoted_quotes]
    }

    # Temukan pemilik kutipan yang dikutip
    quote_owner = quote.user

    if quote_owner:
        # Perbarui poin loyalitas pemilik kutipan
        quote_owner.loyalty_point += 100
        quote_owner.save()
        return JsonResponse({"status": True, "message": "Berhasil mengutip quote", "quote": context}, status=200)

    return JsonResponse({"status": False, "message": "Terjadi kesalahan"}, status=500)

# def show_json(request): #nampilin code dalam bentuk json
#     data = Quote.objects.all()
#     return HttpResponse(serialize("json", data), content_type="application/json")

def show_json(request):
    quotes = Quote.objects.all()
    quotes_json = json.loads(serialize('json', quotes))

    # Tambahkan username ke setiap quote
    for quote in quotes_json:
        user_id = quote['fields']['user']
        username = User.objects.get(id=user_id).username
        quote['fields']['username'] = username

    return HttpResponse(json.dumps(quotes_json), content_type="application/json")

def show_json_by_id(request, id):
    data = Quote.objects.filter(pk=id)
    return HttpResponse(serialize("json", data), content_type="application/json")

# def show_json(request):
#     quotes = Quote.objects.all()
#     serializer = QuoteSerializer(quotes, many=True)
#     return JsonResponse(serializer.data, safe=False)

# def show_json_by_id(request, id):
#     try:
#         quote = Quote.objects.get(pk=id)
#     except Quote.DoesNotExist:
#         return JsonResponse({'error': 'Quote not found'}, status=404)
#     serializer = QuoteSerializer(quote)
#     return JsonResponse(serializer.data)

# def show_json(request):
#     # Ambil semua data dari model Quote
#     quotes_data = Quote.objects.all()
    
#     # Ambil semua data dari model QuoteCited
#     quoted_data = QuoteCited.objects.all()
    
#     # Serialisasi data dari kedua model
#     quotes_json = serialize("json", quotes_data)
#     quoted_json = serialize("json", quoted_data)

#     # Gabungkan hasil serialisasi
#     combined_data = quotes_json + quoted_json
    
#     return JsonResponse(combined_data, safe=False, content_type="application/json")

# def show_json_by_id(request, id):
#     # Ambil data dari model Quote berdasarkan ID
#     quote_data = Quote.objects.filter(pk=id)
    
#     # Ambil data dari model QuoteCited berdasarkan ID
#     quoted_data = QuoteCited.objects.filter(pk=id)
    
#     # Serialisasi data dari kedua model
#     quote_json = serialize("json", quote_data)
#     quoted_json = serialize("json", quoted_data)

#     # Gabungkan hasil serialisasi
#     combined_data = quote_json + quoted_json
    
#     return JsonResponse(combined_data, safe=False, content_type="application/json")