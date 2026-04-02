from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.liste_mouvements, name='liste'),
    path('entree/', views.entree_stock, name='entree'),
    path('historique/', views.historique, name='historique'),
]