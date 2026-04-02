from django.urls import path
from . import views

app_name = 'depenses'

urlpatterns = [
    path('', views.liste_depenses, name='liste'),
    path('ajouter/', views.ajouter_depense, name='ajouter'),
    path('<int:pk>/supprimer/', views.supprimer_depense, name='supprimer'),
]