from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quotes.models import Quote, QuoteCited
from django.http import HttpResponseRedirect, HttpResponseBadRequest
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
        quote_owner.loyalty_point += 1000
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

    return JsonResponse({'error': 'AJAX ga valid'})