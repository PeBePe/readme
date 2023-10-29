from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quotes.models import Quote, QuoteCited
from django.http import HttpResponseRedirect
from django.urls import reverse
from quotes.forms import ProductForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from readme.models import User

# Create your views here.

@login_required(login_url='/landing-page', redirect_field_name=None) #biar main cuma bisa diakses sama user yang udah login
def index(request):
    user = request.user
    quotes = Quote.objects.all() #ambil semua quotes yang ada
    quotes_count = quotes.count() #menghitung jumlah quotes yang ada
    quoted_quotes = QuoteCited.objects.select_related('quote_id', 'user_id').all()  #ngambil daftar kutipan dan pengguna yang mengutipnya

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

    if form.is_valid() and request.method == "POST": #validasi isi form
        product = form.save(commit=False) #biar objek ga langsung disimpen di database
        product.user = request.user
        product.save()
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

    #set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        #form disimpan dan balik ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('quotes'))
    
    context = {'form':form}
    return render(request, "quotes/edit_quotes.html", context)

def cited_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)

    # Menghitung berapa banyak user yg telah mengutip suatu quote
    cited_count = QuoteCited.objects.filter(quote_id=quote).count()

    #cek apakah user udah cited suatu quote atau belum
    user_cited = QuoteCited.objects.filter(quote_id=quote, user_id=request.user).exists()

    if request.method == "POST":
        #cek jumlah cited udah lebih dari 3 atau belum
        if not user_cited and cited_count <= 3:
            QuoteCited.objects.create(quote_id=quote, user_id=request.user)
            cited_count += 1 #tambah jumlah cited quote

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
        return redirect ('quotes')

    return render(request, 'quotes/cited_quote.html', context)