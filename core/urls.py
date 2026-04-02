from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import splash_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash_view, name='splash'),
    path('accounts/', include('accounts.urls')),
    path('', include('produits.urls')),
    path('stock/', include('stock.urls')),
    path('ventes/', include('ventes.urls')),
    path('rapports/', include('rapports.urls')),
    path('depenses/', include('depenses.urls')),
    path('sync/', include('sync.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)