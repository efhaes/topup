from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_products, name='game_products'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('success/<int:transaction_id>/', views.transaction_success, name='transaction_success'),
]

# Menambahkan pengaturan media file (hanya aktif di development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
