from django import forms
from django.contrib.auth.models import User
from .models import Transaction
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password dan konfirmasi password tidak cocok.")

        
# Form untuk registrasi pengguna
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Form untuk transaksi (checkout)from django.core.exceptions import ValidationError


class TransactionForm(forms.Form):
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
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, required=True)
    ewallet = forms.ChoiceField(choices=E_WALLET_CHOICES, required=False)
    bank = forms.ChoiceField(choices=BANK_CHOICES, required=False)

    game_id = forms.CharField(max_length=100, required=True)
    zone_id = forms.CharField(max_length=100, required=True)
    
    def clean_bank(self):
        payment_method = self.cleaned_data.get('payment_method')
        bank = self.cleaned_data.get('bank')
        # Validasi untuk memastikan bank hanya dipilih saat Bank Transfer
        if payment_method == 'Bank Transfer' and not bank:
            raise forms.ValidationError('Silakan pilih bank transfer.')
        return bank

    def clean_game_id(self):
        game_id = self.cleaned_data.get('game_id')
        # Validasi Game ID jika diperlukan (misalnya panjang ID atau format tertentu)
        if len(game_id) < 5:  # Ganti dengan logika validasi sesuai kebutuhan
            raise ValidationError("Game ID terlalu pendek.")
        return game_id

    def clean_zone_id(self):
        zone_id = self.cleaned_data.get('zone_id')
        # Validasi Zone ID jika diperlukan
        if len(zone_id) < 3:
            raise ValidationError("Zone ID terlalu pendek.")
        return zone_id


    class Meta:
        model = Transaction
        fields = ['game_id', 'zone_id', 'payment_method']
