from django.contrib import admin
from .models import Game, Product, Transaction

# Gunakan satu cara pendaftaran untuk model Game dan Product
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    fields = ('name', 'description', 'image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'game', 'image')

# Hanya satu kali mendaftarkan Transaction
admin.site.register(Transaction)
