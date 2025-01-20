from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hok_tokens', 'Hok Tokens'),
        ('mlbb_diamonds', 'MLBB Diamonds'),
        ('pubg_uc', 'PUBG UC'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    diamond_amount = models.IntegerField()  # Jumlah diamond
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)# Harga produk

    def __str__(self):
        return f"{self.game.name} - {self.diamond_amount} Diamonds"



class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ('E-wallet', 'E-wallet'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    E_WALLET_CHOICES = [
        ('DANA', 'DANA'),
        ('OVO', 'OVO'),
        ('GoPay', 'GoPay'),
    ]

    BANK_CHOICES = [
        ('BRI', 'BRI'),
        ('BCA', 'BCA'),
        ('BTN', 'BTN'),
        # Tambahkan bank lain jika diperlukan
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    game_id = models.CharField(max_length=100)
    zone_id = models.CharField(max_length=100)
    email = models.EmailField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    ewallet = models.CharField(max_length=50, choices=E_WALLET_CHOICES, blank=True, null=True)
    bank = models.CharField(max_length=50, choices=BANK_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} - {self.status}"



