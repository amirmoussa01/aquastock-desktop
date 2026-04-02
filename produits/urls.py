from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_redirect'),  # ← Ajoute
    path('produits/', views.liste_produits, name='liste'),
    path('produits/ajouter/', views.ajouter_produit, name='ajouter'),
    path('produits/<int:pk>/modifier/', views.modifier_produit, name='modifier'),
    path('produits/<int:pk>/supprimer/', views.supprimer_produit, name='supprimer'),
    path('categories/', views.liste_categories, name='categories'),
]