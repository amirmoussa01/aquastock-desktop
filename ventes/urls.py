from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    path('', views.liste_ventes, name='liste'),
    path('nouvelle/', views.nouvelle_vente, name='nouvelle'),
    path('<int:pk>/ticket/', views.ticket_vente, name='ticket'),
    path('<int:pk>/annuler/', views.annuler_vente, name='annuler'),
]