from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  # Menambahkan import untuk messages
from django.contrib.auth.models import User  # Menambahkan import untuk User
from .models import Game, Product, Transaction
from .forms import TransactionForm


# Registrasi
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'registrasi/login.html')


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email'] 

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username sudah digunakan.')
        else:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')

    return render(request, 'registrasi/registrasi.html')

# Logout
@login_required
def user_logout(request):
    logout(request)  # Logout user yang sedang aktif
    return redirect('home')  # Redirect ke home setelah logout

# Halaman Home
def home(request):
    games = Game.objects.all()  # Ambil semua game dari database
    return render(request, 'home.html', {'games': games})

# Menampilkan produk berdasarkan game
def game_products(request, game_id):
    game = get_object_or_404(Game, id=game_id)  # Ambil data game berdasarkan ID
    products = Product.objects.filter(game=game)
    if not request.user.is_authenticated:
        messages.info(request, 'Silakan login untuk membeli produk.')
        # Ambil produk berdasarkan game yang dipilih
    return render(request, 'products.html', {'game': game, 'products': products})

# Proses checkout produk
@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            user = request.user
            game_id = form.cleaned_data['game_id']
            zone_id = form.cleaned_data['zone_id']
            email = user.email

            # Tentukan metode pembayaran dan pilihan bank/ewallet
            if payment_method == "E-wallet":
                ewallet = form.cleaned_data['ewallet']
                payment_details = ewallet  # Menyimpan ewallet yang dipilih
            elif payment_method == "Bank Transfer":
                bank = form.cleaned_data['bank']
                payment_details = bank  # Menyimpan bank yang dipilih
            else:
                payment_details = None

            # Simpan transaksi
            transaction = Transaction(
                user=user,
                product=product,
                game_id=game_id,
                zone_id=zone_id,
                payment_method=payment_method,
                email=email,
                status='Pending',  # Status default
            )

            # Jika ada pilihan bank atau ewallet, simpan dalam transaksi
            if payment_method == "Bank Transfer" and payment_details:
                transaction.bank = payment_details
            elif payment_method == "E-wallet" and payment_details:
                transaction.ewallet = payment_details

            transaction.save()

            # Simulasi pembayaran berhasil
            transaction.status = 'Completed'  # Ganti status menjadi completed setelah simulasikan pembayaran
            transaction.save()

            # Redirect ke halaman sukses transaksi
            return redirect('transaction_success', transaction_id=transaction.id)

    else:
        form = TransactionForm()

    return render(request, 'checkout.html', {'product': product, 'form': form})



# Halaman sukses setelah transaksi
@login_required
def transaction_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    return render(request, 'checout_success.html', {'transaction': transaction})

